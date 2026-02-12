from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import PostLike, BlogPost
from comments.models import Comment, CommentLike, Notification


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Create notification when someone replies to a comment"""
    if created and instance.parent:
        # Check if replying to own comment
        parent_is_same_user = False
        
        if instance.author and instance.parent.author:
            # Both are logged-in users
            parent_is_same_user = instance.author == instance.parent.author
        elif not instance.author and not instance.parent.author:
            # Both are guests - check email
            if instance.guest_email and instance.parent.guest_email:
                parent_is_same_user = instance.guest_email.lower() == instance.parent.guest_email.lower()
        
        # Create notification only if replying to someone else and parent has an account
        if not parent_is_same_user and instance.parent.author:
            author_name = instance.author.get_full_name() if instance.author else instance.guest_name
            content_obj = instance.content_object
            post_title = getattr(content_obj, 'title', 'a post') if content_obj else 'a post'
            Notification.objects.create(
                recipient=instance.parent.author,
                sender=instance.author,  # Can be None for guest users
                sender_name_cache=author_name or 'Someone',
                notification_type='comment_reply',
                content_type=instance.content_type,
                object_id=instance.object_id,
                comment=instance.parent,
                message=f'{author_name} replied to your comment on "{post_title}"'
            )


@receiver(post_save, sender=PostLike)
def create_post_like_notification(sender, instance, created, **kwargs):
    """Create notification when someone likes a post"""
    if created and instance.user != instance.post.author:
        sender_name = instance.user.get_full_name() or instance.user.username
        post_ct = ContentType.objects.get_for_model(BlogPost)
        # Someone liked the post
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.user,
            sender_name_cache=sender_name,
            notification_type='post_like',
            content_type=post_ct,
            object_id=instance.post.id,
            message=f'{sender_name} liked your post "{instance.post.title}"'
        )


@receiver(post_save, sender=CommentLike)
def create_comment_like_notification(sender, instance, created, **kwargs):
    """Create notification when someone likes a comment"""
    if created and instance.comment.author and instance.user != instance.comment.author:
        sender_name = instance.user.get_full_name() or instance.user.username if instance.user else 'Someone'
        content_obj = instance.comment.content_object
        post_title = getattr(content_obj, 'title', 'a post') if content_obj else 'a post'
        # Someone liked the comment
        Notification.objects.create(
            recipient=instance.comment.author,
            sender=instance.user,
            sender_name_cache=sender_name,
            notification_type='comment_like',
            content_type=instance.comment.content_type,
            object_id=instance.comment.object_id,
            comment=instance.comment,
            message=f'{sender_name} liked your comment on "{post_title}"'
        )
