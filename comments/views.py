from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.contenttypes.models import ContentType
from .models import Comment, CommentLike, CommentEditHistory


@require_http_methods(["POST"])
@login_required
def edit_comment(request, comment_id):
    """Edit an existing comment (only by author)"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check permission
    if comment.author != request.user:
        return JsonResponse({'success': False, 'error': 'You can only edit your own comments.'}, status=403)
    
    new_content = request.POST.get('content', '').strip()
    if not new_content:
        return JsonResponse({'success': False, 'error': 'Comment cannot be empty.'})
    
    # Save edit history
    if comment.content != new_content:
        CommentEditHistory.objects.create(
            comment=comment,
            previous_content=comment.content,
            edited_by=request.user
        )
        
        comment.content = new_content
        comment.is_edited = True
        comment.save(update_fields=['content', 'is_edited', 'updated_at'])
    
    return JsonResponse({
        'success': True,
        'content': comment.content,
        'is_edited': comment.is_edited,
        'updated_at': comment.updated_at.strftime('%B %d, %Y at %I:%M %p')
    })


@require_http_methods(["POST"])
@login_required
def toggle_like_comment(request, comment_id):
    """Toggle like on a comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    like, created = CommentLike.objects.get_or_create(
        comment=comment,
        user=request.user
    )
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'like_count': comment.get_like_count()
    })


@require_http_methods(["GET"])
def get_edit_history(request, comment_id):
    """Get edit history for a comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    history = comment.edit_history.all()[:10]  # Last 10 edits
    
    history_data = [{
        'previous_content': edit.previous_content,
        'edited_at': edit.edited_at.strftime('%B %d, %Y at %I:%M %p'),
        'edited_by': edit.edited_by.username if edit.edited_by else 'Unknown'
    } for edit in history]
    
    return JsonResponse({
        'success': True,
        'history': history_data,
        'current_content': comment.content
    })

