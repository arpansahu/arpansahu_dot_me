from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, CommentLike, Notification


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """
    Create notifications when:
    1. Someone replies to your comment
    2. Someone comments on your post (for content owners)
    """
    if not created:
        return
    
    # Notify parent comment author when someone replies
    if instance.parent and instance.parent.author:
        # Don't notify yourself
        if instance.author != instance.parent.author:
            sender_name = instance.get_author_display_name()
            Notification.objects.create(
                recipient=instance.parent.author,
                sender=instance.author,
                sender_name_cache=sender_name,
                notification_type='comment_reply',
                comment=instance,
                message=f'{sender_name} replied to your comment'
            )
    
    # TODO: Notify content owner (requires generic relation to content_object)
    # This would require accessing the content_object and checking if it has an owner


@receiver(post_save, sender=CommentLike)
def create_like_notification(sender, instance, created, **kwargs):
    """Create notification when someone likes your comment"""
    if not created:
        return
    
    comment_author = instance.comment.author
    
    # Only notify if comment has an author and it's not self-like
    if comment_author and instance.user != comment_author:
        sender_name = instance.user.get_full_name() or instance.user.username if instance.user else 'Someone'
        Notification.objects.create(
            recipient=comment_author,
            sender=instance.user,
            sender_name_cache=sender_name,
            notification_type='comment_like',
            comment=instance.comment,
            message=f'{sender_name} liked your comment'
        )
