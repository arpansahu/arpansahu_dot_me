from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count, Prefetch
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import BlogPost, Category, Tag, PostLike
from comments.models import Comment, CommentLike, Notification
from account.models import Account


def _get_sidebar_categories(current_post=None):
    """Build sidebar data: categories with their posts in sequence order."""
    categories_with_posts = Category.objects.prefetch_related(
        Prefetch(
            'posts',
            queryset=BlogPost.objects.filter(
                status='published',
                author__is_active=True
            ).order_by('sequence', 'published_date').only(
                'id', 'title', 'slug', 'sequence', 'category_id'
            ),
            to_attr='ordered_posts'
        )
    ).annotate(
        published_post_count=Count(
            'posts',
            filter=Q(posts__status='published', posts__author__is_active=True)
        )
    ).filter(published_post_count__gt=0).order_by('name')

    return categories_with_posts


def blog_list(request):
    """List all published blog posts"""
    # Only show posts from active authors
    posts = BlogPost.objects.filter(
        status='published',
        author__is_active=True
    ).select_related('author', 'category').prefetch_related('tags')
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Filter by tag
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Search
    search_query = request.GET.get('q')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories and tags for sidebar
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    
    # Get featured posts (only from active authors)
    featured_posts = BlogPost.objects.filter(status='published', is_featured=True, author__is_active=True)[:3]
    
    # Sidebar: categories with ordered posts
    sidebar_categories = _get_sidebar_categories()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'featured_posts': featured_posts,
        'search_query': search_query,
        'sidebar_categories': sidebar_categories,
    }
    
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    """Display a single blog post"""
    post = get_object_or_404(
        BlogPost.objects.select_related('author', 'category').prefetch_related('tags'),
        slug=slug,
        status='published',
        author__is_active=True  # Only show posts from active authors
    )
    
    # Increment views
    post.increment_views()
    
    # Get approved comments (only top-level, replies will be nested)
    approved_comments = post.comments.filter(is_approved=True, parent=None).select_related('author').prefetch_related('replies__author')
    
    # Get related posts (same category or tags, only from active authors)
    related_posts = BlogPost.objects.filter(
        status='published',
        author__is_active=True
    ).filter(
        Q(category=post.category) | Q(tags__in=post.tags.all())
    ).exclude(
        id=post.id
    ).distinct()[:5]
    
    # Get all categories for sidebar
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    
    # Sidebar: categories with ordered posts
    sidebar_categories = _get_sidebar_categories(current_post=post)
    
    # Find previous and next posts within same category (series)
    prev_post = None
    next_post = None
    series_posts = []
    if post.category:
        same_category_posts = list(BlogPost.objects.filter(
            status='published',
            author__is_active=True,
            category=post.category
        ).order_by('sequence', 'published_date').values_list('id', 'title', 'slug', flat=False))
        
        # Build series_posts list with current flag
        for i, (pid, ptitle, pslug) in enumerate(same_category_posts):
            series_posts.append({
                'title': ptitle,
                'slug': pslug,
                'is_current': pid == post.id,
                'number': i + 1,
            })
        
        current_index = None
        for i, (pid, ptitle, pslug) in enumerate(same_category_posts):
            if pid == post.id:
                current_index = i
                break
        
        if current_index is not None:
            if current_index > 0:
                p = same_category_posts[current_index - 1]
                prev_post = {'title': p[1], 'slug': p[2]}
            if current_index < len(same_category_posts) - 1:
                n = same_category_posts[current_index + 1]
                next_post = {'title': n[1], 'slug': n[2]}
    
    context = {
        'post': post,
        'approved_comments': approved_comments,
        'related_posts': related_posts,
        'categories': categories,
        'sidebar_categories': sidebar_categories,
        'prev_post': prev_post,
        'next_post': next_post,
        'series_posts': series_posts,
    }
    
    return render(request, 'blog/blog_detail.html', context)


def add_comment(request, post_slug):
    """Add a comment or reply to a blog post (AJAX)"""
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, slug=post_slug, status='published')
        
        if not post.enable_comments:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Comments are disabled for this post.'})
            messages.error(request, 'Comments are disabled for this post.')
            return redirect('blog:blog_detail', slug=post_slug)
        
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')
        
        if not content:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Comment cannot be empty.'})
            messages.error(request, 'Comment cannot be empty.')
            return redirect('blog:blog_detail', slug=post_slug)
        
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id)
        
        # Handle both logged-in and guest users
        if request.user.is_authenticated:
            comment = Comment.objects.create(
                content_object=post,
                author=request.user,
                parent=parent,
                content=content,
                is_approved=True  # Auto-approve for logged-in users
            )
        else:
            # Guest user
            guest_name = request.POST.get('guest_name', '').strip()
            guest_email = request.POST.get('guest_email', '').strip()
            
            if not guest_name:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Please provide your name.'})
                messages.error(request, 'Please provide your name.')
                return redirect('blog:blog_detail', slug=post_slug)
            
            comment = Comment.objects.create(
                content_object=post,
                guest_name=guest_name,
                guest_email=guest_email,
                parent=parent,
                content=content,
                is_approved=False  # Require approval for guests
            )
        
        # AJAX response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'author': comment.get_author_display_name(),
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p'),
                    'is_approved': comment.is_approved,
                    'is_logged_in': request.user.is_authenticated
                },
                'message': 'Comment posted successfully!' if comment.is_approved else 'Your comment is awaiting approval.'
            })
        
        # Non-AJAX response
        if comment.is_approved:
            messages.success(request, 'Comment posted successfully!')
        else:
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
    
    return redirect('blog:blog_detail', slug=post_slug)


@login_required
def toggle_post_like(request, post_slug):
    """Toggle like on a blog post"""
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, slug=post_slug, status='published')
        like, created = PostLike.objects.get_or_create(post=post, user=request.user)
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'like_count': post.get_like_count()
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def toggle_comment_like(request, comment_id):
    """Toggle like on a comment"""
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id, is_approved=True)
        like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'like_count': comment.get_like_count()
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def category_posts(request, slug):
    """List posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(status='published', category=category).select_related('author', 'category')
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/category_posts.html', context)


def tag_posts(request, slug):
    """List posts by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = BlogPost.objects.filter(status='published', tags=tag).select_related('author', 'category')
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/tag_posts.html', context)


def user_profile(request, username):
    """Display user profile with their activity"""
    user = get_object_or_404(Account, username=username)
    
    # Get user's published posts
    posts = BlogPost.objects.filter(author=user, status='published').order_by('-published_date')[:10]
    
    # Get user's approved comments (without select_related since GenericForeignKey)
    comments = Comment.objects.filter(author=user, is_approved=True).select_related('author', 'content_type').order_by('-created_at')[:20]
    
    # Get stats
    total_posts = BlogPost.objects.filter(author=user, status='published').count()
    total_comments = Comment.objects.filter(author=user, is_approved=True).count()
    total_post_likes = PostLike.objects.filter(post__author=user).count()
    
    context = {
        'profile_user': user,
        'posts': posts,
        'comments': comments,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_post_likes': total_post_likes,
    }
    
    return render(request, 'blog/user_profile.html', context)


@login_required
def notifications(request):
    """Display user notifications"""
    user_notifications = request.user.notifications.all()[:50]
    
    # Mark as read
    unread = user_notifications.filter(is_read=False)
    unread_count = unread.count()
    
    context = {
        'notifications': user_notifications,
        'unread_count': unread_count,
    }
    
    return render(request, 'blog/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    
    return redirect(notification.get_url())


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    if request.method == 'POST':
        request.user.notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
    
    return redirect('blog:notifications')
