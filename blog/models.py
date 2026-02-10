from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from account.models import Account
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Blog post tags"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Main blog post model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='blog_posts')
    
    # Content
    excerpt = models.TextField(max_length=500, help_text="Short description for preview")
    content = RichTextUploadingField(help_text="Main content with rich text editor")
    
    # Featured image
    featured_image = models.ImageField(upload_to='blog/featured/', blank=True, null=True)
    
    # Metadata
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Status and dates
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Stats
    views = models.PositiveIntegerField(default=0)
    
    # Settings
    enable_comments = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Display on homepage")
    
    # Generic relation to comments
    comments = GenericRelation('comments.Comment', related_query_name='blog_posts')
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def get_reading_time(self):
        """Calculate estimated reading time in minutes"""
        word_count = len(self.content.split())
        reading_time = word_count / 200  # Average reading speed
        return max(1, round(reading_time))
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_like_count(self):
        """Get total likes for this post"""
        return self.likes.count()
    
    def is_liked_by(self, user):
        """Check if user has liked this post"""
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False


class PostLike(models.Model):
    """Likes for blog posts"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'

