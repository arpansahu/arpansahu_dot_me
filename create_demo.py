from blog.models import BlogPost, Category, Tag
from account.models import Account
from django.utils import timezone

author = Account.objects.filter(is_superuser=True).first()
if not author:
    print("No superuser found!")
else:
    category, _ = Category.objects.get_or_create(
        slug='technology',
        defaults={'name': 'Technology', 'description': 'Tech tutorials'}
    )
    
    python_tag, _ = Tag.objects.get_or_create(slug='python', defaults={'name': 'Python'})
    django_tag, _ = Tag.objects.get_or_create(slug='django', defaults={'name': 'Django'})
    
    post, created = BlogPost.objects.get_or_create(
        slug='welcome-to-my-blog',
        defaults={
            'title': 'Welcome to My Blog - Interactive Demo',
            'author': author,
            'content': '<h2>Welcome to My Blog!</h2><p>This demo post showcases <strong>likes</strong>, <strong>nested comments</strong>, and <strong>code highlighting</strong>!</p><h3>Features</h3><ul><li>Like posts and comments</li><li>Reply to comments</li><li>User profiles</li><li>Notifications</li></ul><pre><code class="language-python">def hello():\n    print("Hello, World!")</code></pre>',
            'excerpt': 'Discover interactive features: likes, nested comments, user profiles, and real-time notifications!',
            'category': category,
            'status': 'published',
            'published_date': timezone.now(),
            'is_featured': True,
            'enable_comments': True,
            'meta_description': 'Demo blog post with interactive features',
        }
    )
    
    if created:
        post.tags.add(python_tag, django_tag)
        print(f"✅ Created: {post.title}")
        print(f"   URL: /blog/post/{post.slug}/")
    else:
        print(f"ℹ️  Post already exists: {post.title}")
