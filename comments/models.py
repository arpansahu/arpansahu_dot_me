from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from account.models import Account


class Comment(models.Model):
    """
    Universal comment model that can be attached to any model using Generic Relations.
    Supports nested threading (replies to replies) and guest commenting.
    """
    # Generic relation to any model (BlogPost, Project, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Author (registered or guest)
    author = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE, 
        related_name='comments', 
        null=True, 
        blank=True,
        help_text="Registered user who made the comment"
    )
    
    # Guest user fields
    guest_name = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Name for non-logged-in users"
    )
    guest_email = models.EmailField(
        blank=True, 
        help_text="Email for notifications (not displayed publicly)"
    )
    
    # Threading support - unlimited depth
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='replies',
        help_text="Parent comment for nested threads"
    )
    
    # Comment content
    content = models.TextField(help_text="Comment text content")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(
        default=False, 
        help_text="Requires approval for guest comments"
    )
    is_edited = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False, help_text="Pin important comments")
    
    class Meta:
        ordering = ['-is_pinned', 'created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id', 'created_at']),
            models.Index(fields=['parent']),
            models.Index(fields=['is_approved']),
        ]
    
    def __str__(self):
        author_name = self.get_author_display_name()
        content_preview = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return f'Comment by {author_name}: {content_preview}'
    
    def get_author_display_name(self):
        """Get display name for comment author"""
        if self.author:
            return self.author.get_full_name() or self.author.username
        return self.guest_name or 'Anonymous'
    
    def get_like_count(self):
        """Get total likes for this comment"""
        return self.likes.count()
    
    def is_liked_by(self, user):
        """Check if user has liked this comment"""
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False
    
    def get_reply_count(self):
        """Get total replies to this comment"""
        return self.replies.filter(is_approved=True).count()
    
    def get_thread_depth(self):
        """Calculate depth level in comment thread"""
        depth = 0
        current = self.parent
        while current:
            depth += 1
            current = current.parent
        return depth
    
    def save(self, *args, **kwargs):
        # Auto-approve comments from registered users
        if self.author and not self.pk:  # New comment from registered user
            self.is_approved = True
        super().save(*args, **kwargs)


class CommentLike(models.Model):
    """Likes for comments"""
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    user = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE, 
        related_name='user_comment_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['comment', 'user']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['comment', 'created_at']),
        ]
    
    def __str__(self):
        return f'{self.user.username} likes comment {self.comment.id}'


class CommentEditHistory(models.Model):
    """Track edit history for comments"""
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='edit_history'
    )
    previous_content = models.TextField(help_text="Content before edit")
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='comment_edits'
    )
    
    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = 'Comment edit histories'
    
    def __str__(self):
        return f'Edit of comment {self.comment.id} at {self.edited_at}'


class Notification(models.Model):
    """
    User notifications for comments, replies, and interactions
    """
    NOTIFICATION_TYPES = [
        ('comment_reply', 'Comment Reply'),
        ('comment_like', 'Comment Like'),
        ('comment_mention', 'Mentioned in Comment'),
        ('post_comment', 'New Comment on Your Post'),
    ]
    
    recipient = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE, 
        related_name='user_notifications'
    )
    sender = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE, 
        related_name='user_sent_notifications', 
        null=True, 
        blank=True,
        help_text="User who triggered the notification (null for guest users)"
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    # Generic relation for flexible notification targets
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Direct relation to comment for backwards compatibility
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['is_read']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f'{self.notification_type} for {self.recipient.username}'
    
    def get_url(self):
        """Get URL to the related content"""
        if self.content_object:
            return getattr(self.content_object, 'get_absolute_url', lambda: '#')()
        return '#'
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
