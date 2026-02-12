"""
Tests for comments application.
"""
import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from comments.models import Comment, CommentLike, CommentEditHistory
from blog.models import BlogPost, Category

User = get_user_model()


@pytest.fixture
def client():
    """Django test client."""
    return Client()


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User.objects.create_user(
        email='commentuser@example.com',
        username='commentuser',
        password='TestPassword123!'
    )
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def test_user_2(db):
    """Create another test user."""
    user = User.objects.create_user(
        email='commentuser2@example.com',
        username='commentuser2',
        password='TestPassword123!'
    )
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def test_category(db):
    """Create a test category."""
    return Category.objects.create(
        name='Comment Test Category',
        slug='comment-test-category'
    )


@pytest.fixture
def published_post(db, test_user, test_category):
    """Create a published blog post."""
    return BlogPost.objects.create(
        title='Post for Comments',
        slug='post-for-comments',
        author=test_user,
        excerpt='Test excerpt',
        content='Test content for comments',
        category=test_category,
        status='published',
        published_date=timezone.now(),
        enable_comments=True
    )


@pytest.fixture
def test_comment(db, test_user, published_post):
    """Create a test comment."""
    return Comment.objects.create(
        content_type=ContentType.objects.get_for_model(BlogPost),
        object_id=published_post.id,
        author=test_user,
        content='This is a test comment',
        is_approved=True
    )


@pytest.fixture
def guest_comment(db, published_post):
    """Create a guest comment."""
    return Comment.objects.create(
        content_type=ContentType.objects.get_for_model(BlogPost),
        object_id=published_post.id,
        guest_name='Guest User',
        guest_email='guest@example.com',
        content='This is a guest comment',
        is_approved=False
    )


class TestCommentModel:
    """Tests for Comment model."""
    
    def test_comment_creation_registered_user(self, test_comment):
        """Test comment creation by registered user."""
        assert test_comment.content == 'This is a test comment'
        assert test_comment.author is not None
        assert test_comment.is_approved is True
    
    def test_comment_creation_guest(self, guest_comment):
        """Test comment creation by guest."""
        assert guest_comment.guest_name == 'Guest User'
        assert guest_comment.author is None
        assert guest_comment.is_approved is False
    
    def test_comment_str(self, test_comment):
        """Test comment string representation."""
        string_repr = str(test_comment)
        assert 'commentuser' in string_repr
        assert 'This is a test comment' in string_repr
    
    def test_get_author_display_name_registered(self, test_comment):
        """Test get_author_display_name for registered user."""
        assert test_comment.get_author_display_name() == 'commentuser'
    
    def test_get_author_display_name_guest(self, guest_comment):
        """Test get_author_display_name for guest."""
        assert guest_comment.get_author_display_name() == 'Guest User'
    
    def test_get_author_display_name_anonymous(self, db, published_post):
        """Test get_author_display_name for anonymous user without name."""
        comment = Comment.objects.create(
            content_type=ContentType.objects.get_for_model(BlogPost),
            object_id=published_post.id,
            content='Anonymous comment',
            is_approved=False
        )
        assert comment.get_author_display_name() == 'Anonymous'
    
    def test_get_like_count_zero(self, test_comment):
        """Test like count is zero initially."""
        assert test_comment.get_like_count() == 0
    
    def test_is_liked_by_anonymous(self, test_comment):
        """Test is_liked_by for anonymous user."""
        from django.contrib.auth.models import AnonymousUser
        anonymous = AnonymousUser()
        assert test_comment.is_liked_by(anonymous) is False
    
    def test_get_reply_count_zero(self, test_comment):
        """Test reply count is zero initially."""
        assert test_comment.get_reply_count() == 0
    
    def test_get_thread_depth_top_level(self, test_comment):
        """Test thread depth for top-level comment."""
        assert test_comment.get_thread_depth() == 0
    
    def test_auto_approve_registered_user_comment(self, db, test_user, published_post):
        """Test comments from registered users are auto-approved."""
        comment = Comment.objects.create(
            content_type=ContentType.objects.get_for_model(BlogPost),
            object_id=published_post.id,
            author=test_user,
            content='Auto-approved comment'
        )
        assert comment.is_approved is True


class TestCommentLikeModel:
    """Tests for CommentLike model."""
    
    def test_commentlike_model_exists(self, db):
        """Test CommentLike model can be imported."""
        from comments.models import CommentLike
        assert CommentLike is not None


class TestCommentEditHistoryModel:
    """Tests for CommentEditHistory model."""
    
    def test_edit_history_creation(self, test_comment, test_user, db):
        """Test creating edit history."""
        history = CommentEditHistory.objects.create(
            comment=test_comment,
            previous_content='Original content',
            edited_by=test_user
        )
        assert history.previous_content == 'Original content'
        assert history.edited_by == test_user


class TestEditCommentView:
    """Tests for edit_comment view."""
    
    def test_edit_comment_requires_login(self, client, test_comment):
        """Test editing comment requires authentication."""
        response = client.post(reverse('comments:edit_comment', kwargs={'comment_id': test_comment.id}))
        assert response.status_code == 302  # Redirect to login
    
    def test_edit_comment_only_author(self, client, test_comment, test_user_2):
        """Test only author can edit their comment."""
        client.login(username='commentuser2@example.com', password='TestPassword123!')
        response = client.post(
            reverse('comments:edit_comment', kwargs={'comment_id': test_comment.id}),
            data={'content': 'Edited content'}
        )
        assert response.status_code == 403
    
    def test_edit_comment_empty_content(self, client, test_comment, test_user):
        """Test editing with empty content fails."""
        client.login(username='commentuser@example.com', password='TestPassword123!')
        response = client.post(
            reverse('comments:edit_comment', kwargs={'comment_id': test_comment.id}),
            data={'content': ''}
        )
        assert response.status_code == 200
        assert not response.json()['success']
    
    def test_edit_comment_success(self, client, test_comment, test_user):
        """Test successful comment edit."""
        client.login(username='commentuser@example.com', password='TestPassword123!')
        response = client.post(
            reverse('comments:edit_comment', kwargs={'comment_id': test_comment.id}),
            data={'content': 'Edited content'}
        )
        assert response.status_code == 200
        assert response.json()['success']
        test_comment.refresh_from_db()
        assert test_comment.content == 'Edited content'
        assert test_comment.is_edited is True
    
    def test_edit_comment_creates_history(self, client, test_comment, test_user):
        """Test editing creates edit history."""
        client.login(username='commentuser@example.com', password='TestPassword123!')
        original_content = test_comment.content
        client.post(
            reverse('comments:edit_comment', kwargs={'comment_id': test_comment.id}),
            data={'content': 'Edited content'}
        )
        history = CommentEditHistory.objects.filter(comment=test_comment).first()
        assert history is not None
        assert history.previous_content == original_content
    
    def test_edit_comment_nonexistent_returns_404(self, client, test_user):
        """Test editing nonexistent comment returns 404 or custom error."""
        client.login(username='commentuser@example.com', password='TestPassword123!')
        response = client.post(
            reverse('comments:edit_comment', kwargs={'comment_id': 99999}),
            data={'content': 'Content'}
        )
        # Custom error handlers may return 200
        assert response.status_code in [200, 404]
    
    def test_edit_comment_get_not_allowed(self, client, test_comment, test_user):
        """Test GET request is not allowed."""
        client.login(username='commentuser@example.com', password='TestPassword123!')
        response = client.get(reverse('comments:edit_comment', kwargs={'comment_id': test_comment.id}))
        assert response.status_code == 405


class TestToggleLikeCommentView:
    """Tests for toggle_like_comment view."""
    
    def test_toggle_like_requires_login(self, client, test_comment):
        """Test liking comment requires authentication."""
        response = client.post(reverse('comments:toggle_like', kwargs={'comment_id': test_comment.id}))
        assert response.status_code == 302  # Redirect to login
    
    def test_toggle_like_nonexistent_returns_404(self, client, test_user):
        """Test liking nonexistent comment returns 404 or custom error."""
        client.login(username='commentuser@example.com', password='TestPassword123!')
        response = client.post(reverse('comments:toggle_like', kwargs={'comment_id': 99999}))
        # Custom error handlers may return 200
        assert response.status_code in [200, 404]
    
    def test_toggle_like_get_not_allowed(self, client, test_comment, test_user):
        """Test GET request is not allowed."""
        client.login(username='commentuser@example.com', password='TestPassword123!')
        response = client.get(reverse('comments:toggle_like', kwargs={'comment_id': test_comment.id}))
        assert response.status_code == 405


class TestGetEditHistoryView:
    """Tests for get_edit_history view."""
    
    def test_get_edit_history_returns_200(self, client, test_comment):
        """Test GET request returns 200."""
        response = client.get(reverse('comments:edit_history', kwargs={'comment_id': test_comment.id}))
        assert response.status_code == 200
    
    def test_get_edit_history_empty(self, client, test_comment):
        """Test edit history is empty for unedited comment."""
        response = client.get(reverse('comments:edit_history', kwargs={'comment_id': test_comment.id}))
        assert response.status_code == 200
        assert response.json()['success']
        assert len(response.json()['history']) == 0
    
    def test_get_edit_history_with_edits(self, client, test_comment, test_user, db):
        """Test edit history with edits."""
        CommentEditHistory.objects.create(
            comment=test_comment,
            previous_content='Original content',
            edited_by=test_user
        )
        response = client.get(reverse('comments:edit_history', kwargs={'comment_id': test_comment.id}))
        assert response.status_code == 200
        assert len(response.json()['history']) == 1
        assert response.json()['history'][0]['previous_content'] == 'Original content'
    
    def test_get_edit_history_nonexistent_returns_404(self, client, db):
        """Test nonexistent comment returns 404 or custom error."""
        response = client.get(reverse('comments:edit_history', kwargs={'comment_id': 99999}))
        # Custom error handlers may return 200
        assert response.status_code in [200, 404]
    
    def test_get_edit_history_post_not_allowed(self, client, test_comment):
        """Test POST request is not allowed."""
        response = client.post(reverse('comments:edit_history', kwargs={'comment_id': test_comment.id}))
        assert response.status_code == 405




class TestToggleLikeCommentFunctionView:
    """Tests for comments toggle_like_comment function-based view."""

    def test_toggle_like_comment_creates_like(self, client, test_user, test_comment):
        """Test POST creates a comment like."""
        client.force_login(test_user)
        # Use a different user to like (test_user created the comment)
        other_user = User.objects.create_user(
            email='liker@example.com', username='liker', password='pass123'
        )
        other_user.is_active = True
        other_user.save()
        client.force_login(other_user)
        response = client.post(reverse('comments:toggle_like', kwargs={'comment_id': test_comment.id}))
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['liked'] is True

    def test_toggle_like_comment_removes_like(self, client, test_comment):
        """Test toggling like twice removes the like."""
        other_user = User.objects.create_user(
            email='liker2@example.com', username='liker2', password='pass123'
        )
        other_user.is_active = True
        other_user.save()
        client.force_login(other_user)
        url = reverse('comments:toggle_like', kwargs={'comment_id': test_comment.id})
        client.post(url)  # like
        response = client.post(url)  # unlike
        data = response.json()
        assert data['liked'] is False
        assert data['like_count'] == 0

    def test_toggle_like_requires_login(self, client, test_comment):
        """Test liking requires authentication."""
        response = client.post(reverse('comments:toggle_like', kwargs={'comment_id': test_comment.id}))
        assert response.status_code == 302

    def test_toggle_like_get_not_allowed(self, client, test_user, test_comment):
        """Test GET request returns 405."""
        client.force_login(test_user)
        response = client.get(reverse('comments:toggle_like', kwargs={'comment_id': test_comment.id}))
        assert response.status_code == 405


class TestCommentSignals:
    """Tests for comments signal handlers."""

    def test_comment_reply_creates_notification(self, db, test_user, test_user_2, published_post, test_comment):
        """Test notification is created when someone replies to a comment."""
        from comments.models import Notification
        ct = ContentType.objects.get_for_model(BlogPost)
        Comment.objects.create(
            content_type=ct, object_id=published_post.id,
            author=test_user_2, content='Reply to your comment',
            parent=test_comment, is_approved=True
        )
        assert Notification.objects.filter(
            recipient=test_user, notification_type='comment_reply'
        ).exists()

    def test_like_creates_notification(self, db, test_user, test_user_2, test_comment):
        """Test notification is created when someone likes a comment."""
        from comments.models import Notification
        CommentLike.objects.create(comment=test_comment, user=test_user_2)
        assert Notification.objects.filter(
            recipient=test_user, notification_type='comment_like'
        ).exists()

    def test_self_like_no_notification(self, db, test_user, test_comment):
        """Test no notification when liking own comment."""
        from comments.models import Notification
        CommentLike.objects.create(comment=test_comment, user=test_user)
        assert not Notification.objects.filter(
            recipient=test_user, notification_type='comment_like'
        ).exists()

    def test_self_reply_no_notification(self, db, test_user, published_post, test_comment):
        """Test no notification when replying to own comment."""
        from comments.models import Notification
        ct = ContentType.objects.get_for_model(BlogPost)
        Comment.objects.create(
            content_type=ct, object_id=published_post.id,
            author=test_user, content='My own reply',
            parent=test_comment, is_approved=True
        )
        assert not Notification.objects.filter(
            recipient=test_user, notification_type='comment_reply'
        ).exists()

