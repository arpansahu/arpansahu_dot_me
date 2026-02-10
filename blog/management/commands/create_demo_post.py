from django.core.management.base import BaseCommand
from blog.models import BlogPost, Category, Tag
from account.models import Account
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create a demo blog post'

    def handle(self, *args, **kwargs):
        # Get or create author
        author = Account.objects.filter(is_superuser=True).first()
        
        if not author:
            self.stdout.write(self.style.ERROR('No superuser found. Please create a superuser first.'))
            return

        # Create category
        category, _ = Category.objects.get_or_create(
            slug='technology',
            defaults={
                'name': 'Technology',
                'description': 'Tech tutorials, tips, and insights'
            }
        )

        # Create tags
        python_tag, _ = Tag.objects.get_or_create(slug='python', defaults={'name': 'Python'})
        django_tag, _ = Tag.objects.get_or_create(slug='django', defaults={'name': 'Django'})
        webdev_tag, _ = Tag.objects.get_or_create(slug='web-development', defaults={'name': 'Web Development'})

        # Demo content
        demo_content = """<h2>Welcome to My Blog!</h2>

<p>This is a demo blog post showcasing all the amazing features of this blogging platform. Let me show you what's possible!</p>

<h3>🚀 Interactive Features</h3>

<p>This blog has several interactive features:</p>

<ul>
<li><strong>Like System</strong>: Click the heart icon to like posts and comments</li>
<li><strong>Nested Comments</strong>: Reply to comments to create conversations</li>
<li><strong>Rich Text</strong>: Write beautiful content with the CKEditor</li>
<li><strong>Code Highlighting</strong>: Share code snippets with syntax highlighting</li>
</ul>

<h3>💻 Code Example</h3>

<p>Here's a simple Python function to demonstrate code highlighting:</p>

<pre><code class="language-python">def fibonacci(n):
    # Generate Fibonacci sequence
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence[:n]

print(fibonacci(10))
</code></pre>

<h3>🎨 Django Views Example</h3>

<pre><code class="language-python">from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog/detail.html', {'post': post})
</code></pre>

<h3>📊 Key Features</h3>

<table border="1" style="width: 100%; border-collapse: collapse;">
<thead>
<tr style="background-color: rgba(187, 134, 252, 0.2);">
<th style="padding: 10px;">Feature</th>
<th style="padding: 10px;">Status</th>
<th style="padding: 10px;">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding: 8px;">Rich Text Editor</td>
<td style="padding: 8px;">✅ Active</td>
<td style="padding: 8px;">CKEditor with image uploads</td>
</tr>
<tr>
<td style="padding: 8px;">Code Highlighting</td>
<td style="padding: 8px;">✅ Active</td>
<td style="padding: 8px;">Syntax highlighting</td>
</tr>
<tr>
<td style="padding: 8px;">Like System</td>
<td style="padding: 8px;">✅ Active</td>
<td style="padding: 8px;">Like posts and comments</td>
</tr>
<tr>
<td style="padding: 8px;">Nested Comments</td>
<td style="padding: 8px;">✅ Active</td>
<td style="padding: 8px;">Reply to comments</td>
</tr>
</tbody>
</table>

<h3>🌟 Modern Design</h3>

<p>The blog features a Medium-inspired design with:</p>

<ol>
<li>Clean, minimalist layout</li>
<li>Dark theme with purple accents</li>
<li>Responsive design for mobile</li>
<li>Smooth animations</li>
<li>Professional typography</li>
</ol>

<blockquote>
<p>"Great design is not just what looks good. It's about how it works." - Steve Jobs</p>
</blockquote>

<h3>📝 Try It Out!</h3>

<p>Feel free to:</p>

<ul>
<li>💙 Like this post</li>
<li>💬 Leave a comment below</li>
<li>↩️ Reply to existing comments</li>
<li>🔍 Search for more posts</li>
<li>📂 Browse by categories and tags</li>
</ul>

<p>This blogging platform is built with <strong>Django 4.2</strong>, <strong>CKEditor</strong>, and features a modern admin panel powered by <strong>Django Jazzmin</strong>.</p>

<h3>🎯 What's Next?</h3>

<p>In future posts, I'll be sharing:</p>

<ul>
<li>Django best practices and tips</li>
<li>Python programming tutorials</li>
<li>Web development insights</li>
<li>System design patterns</li>
<li>DevOps and deployment guides</li>
</ul>

<p><strong>Thank you for reading!</strong> Don't forget to like and comment if you found this useful. 🚀</p>"""

        # Create or update post
        post, created = BlogPost.objects.get_or_create(
            slug='welcome-to-my-blog',
            defaults={
                'title': 'Welcome to My Blog - Interactive Features Demo',
                'author': author,
                'content': demo_content,
                'excerpt': 'Discover the amazing interactive features of this blog including likes, nested comments, code highlighting, and more! This demo post showcases everything you can do.',
                'category': category,
                'status': 'published',
                'published_date': timezone.now(),
                'is_featured': True,
                'enable_comments': True,
                'meta_description': 'Demo blog post showcasing interactive features like likes, nested comments, and code highlighting',
                'meta_keywords': 'blog, django, python, web development, tutorial',
            }
        )

        if created:
            post.tags.add(python_tag, django_tag, webdev_tag)
            self.stdout.write(self.style.SUCCESS(f'✅ Created demo blog post: {post.title}'))
            self.stdout.write(self.style.SUCCESS(f'   URL: /blog/post/{post.slug}/'))
        else:
            self.stdout.write(self.style.WARNING(f'ℹ️  Demo post already exists: {post.title}'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Demo blog setup complete!'))
        self.stdout.write(f'📝 Post: {post.title}')
        self.stdout.write(f'📁 Category: {post.category.name}')
        self.stdout.write(f'🏷️  Tags: {", ".join([t.name for t in post.tags.all()])}')
        self.stdout.write(f'⭐ Featured: {post.is_featured}')
        self.stdout.write(f'💬 Comments enabled: {post.enable_comments}')
