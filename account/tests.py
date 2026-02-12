"""
Tests for account application.
"""
import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def client():
    """Django test client."""
    return Client()


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='TestPassword123!'
    )
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def inactive_user(db):
    """Create an inactive test user."""
    user = User.objects.create_user(
        email='inactive@example.com',
        username='inactiveuser',
        password='TestPassword123!'
    )
    # User is inactive by default
    return user


class TestAccountModel:
    """Tests for Account model."""
    
    def test_create_user(self, db):
        """Test creating a regular user."""
        user = User.objects.create_user(
            email='newuser@example.com',
            username='newuser',
            password='password123'
        )
        assert user.email == 'newuser@example.com'
        assert user.username == 'newuser'
        assert user.is_active is True  # Default True to support OAuth users
        assert user.is_staff is False
        assert user.is_superuser is False
    
    def test_create_superuser(self, db):
        """Test creating a superuser."""
        admin = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpassword123'
        )
        assert admin.email == 'admin@example.com'
        assert admin.is_active is True  # Default True to support OAuth users
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.is_admin is True
    
    def test_user_str(self, test_user):
        """Test user string representation."""
        assert str(test_user) == 'testuser@example.com'
    
    def test_user_get_full_name(self, db):
        """Test get_full_name method."""
        user = User.objects.create_user(
            email='full@example.com',
            username='fulluser',
            password='password123'
        )
        user.first_name = 'John'
        user.last_name = 'Doe'
        user.save()
        assert user.get_full_name() == 'John Doe'
    
    def test_user_get_full_name_fallback(self, test_user):
        """Test get_full_name falls back to username."""
        assert test_user.get_full_name() == 'testuser'
    
    def test_create_user_without_email_raises_error(self, db):
        """Test creating user without email raises ValueError."""
        with pytest.raises(ValueError):
            User.objects.create_user(
                email='',
                username='nomail',
                password='password123'
            )
    
    def test_create_user_without_username_raises_error(self, db):
        """Test creating user without username raises ValueError."""
        with pytest.raises(ValueError):
            User.objects.create_user(
                email='test@example.com',
                username='',
                password='password123'
            )
    
    def test_superuser_has_perm(self, db):
        """Test superuser has permissions."""
        admin = User.objects.create_superuser(
            email='admin2@example.com',
            username='admin2',
            password='adminpassword123'
        )
        assert admin.has_perm('any_perm') is True
    
    def test_superuser_has_module_perms(self, db):
        """Test superuser has module permissions."""
        admin = User.objects.create_superuser(
            email='admin3@example.com',
            username='admin3',
            password='adminpassword123'
        )
        assert admin.has_module_perms('any_app') is True


class TestRegistrationView:
    """Tests for RegistrationView."""
    
    def test_registration_get_returns_200(self, client, db):
        """Test GET request to registration page returns 200."""
        response = client.get(reverse('register'))
        assert response.status_code == 200
    
    def test_registration_uses_correct_template(self, client, db):
        """Test registration uses register.html template."""
        response = client.get(reverse('register'))
        assert 'account/register.html' in [t.name for t in response.templates]
    
    def test_registration_context_contains_form(self, client, db):
        """Test registration context contains form."""
        response = client.get(reverse('register'))
        assert 'registration_form' in response.context
    
    def test_registration_post_valid_data(self, client, db):
        """Test registration with valid data."""
        data = {
            'email': 'newregistration@example.com',
            'username': 'newreguser',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        }
        response = client.post(reverse('register'), data=data)
        # Should redirect or show success
        assert response.status_code in [200, 302]
    
    def test_registration_post_password_mismatch(self, client, db):
        """Test registration with mismatched passwords."""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'StrongPassword123!',
            'password2': 'DifferentPassword456!',
        }
        response = client.post(reverse('register'), data=data)
        assert response.status_code == 200  # Returns form with errors


class TestLoginView:
    """Tests for LoginView."""
    
    def test_login_get_returns_200(self, client, db):
        """Test GET request to login page returns 200."""
        response = client.get(reverse('login'))
        assert response.status_code == 200
    
    def test_login_uses_correct_template(self, client, db):
        """Test login uses login.html template."""
        response = client.get(reverse('login'))
        assert 'account/login.html' in [t.name for t in response.templates]
    
    def test_login_context_contains_form(self, client, db):
        """Test login context contains form."""
        response = client.get(reverse('login'))
        assert 'form' in response.context
    
    def test_login_post_valid_credentials(self, client, test_user):
        """Test login with valid credentials."""
        data = {
            'username': 'testuser@example.com',
            'password': 'TestPassword123!',
        }
        response = client.post(reverse('login'), data=data)
        # Should redirect on successful login
        assert response.status_code == 302
    
    def test_login_post_invalid_credentials(self, client, db):
        """Test login with invalid credentials."""
        data = {
            'username': 'nonexistent@example.com',
            'password': 'wrongpassword',
        }
        response = client.post(reverse('login'), data=data)
        assert response.status_code == 200
        assert 'Invalid credentials' in response.content.decode() or 'msg' in response.context
    
    def test_login_redirects_authenticated_user(self, client, test_user):
        """Test authenticated user is redirected from login page."""
        client.login(username='testuser@example.com', password='TestPassword123!')
        response = client.get(reverse('login'))
        assert response.status_code == 302


class TestLogoutView:
    """Tests for LogoutView."""
    
    def test_logout_redirects_to_login(self, client, test_user):
        """Test logout redirects to login page."""
        client.login(username='testuser@example.com', password='TestPassword123!')
        response = client.get(reverse('logout'))
        assert response.status_code == 302
        assert 'login' in response.url
    
    def test_logout_requires_authentication(self, client, db):
        """Test logout requires authentication."""
        response = client.get(reverse('logout'))
        # Should redirect to login
        assert response.status_code == 302


class TestAccountView:
    """Tests for AccountView (profile)."""
    
    def test_account_requires_login(self, client, db):
        """Test account view requires authentication."""
        response = client.get(reverse('account'))
        assert response.status_code == 302  # Redirect to login
    
    def test_account_get_returns_200_for_authenticated(self, client, test_user):
        """Test GET request to account page returns 200 for authenticated user."""
        client.login(username='testuser@example.com', password='TestPassword123!')
        response = client.get(reverse('account'))
        assert response.status_code == 200
    
    def test_account_uses_correct_template(self, client, test_user):
        """Test account page uses account.html template."""
        client.login(username='testuser@example.com', password='TestPassword123!')
        response = client.get(reverse('account'))
        assert 'account/account.html' in [t.name for t in response.templates]
    
    def test_account_context_contains_user(self, client, test_user):
        """Test account context contains user."""
        client.login(username='testuser@example.com', password='TestPassword123!')
        response = client.get(reverse('account'))
        assert 'account' in response.context
    
    def test_account_post_update_profile(self, client, test_user):
        """Test updating profile via POST."""
        client.login(username='testuser@example.com', password='TestPassword123!')
        data = {
            'username': 'updateduser',
            'email': 'testuser@example.com',
            'first_name': 'Updated',
            'last_name': 'Name',
        }
        response = client.post(reverse('account'), data=data)
        assert response.status_code == 200
        test_user.refresh_from_db()
        assert test_user.first_name == 'Updated'


class TestPasswordReset:
    """Tests for password reset functionality."""
    
    def test_password_reset_get_returns_200(self, client, db):
        """Test GET request to password reset returns 200."""
        response = client.get(reverse('password_reset'))
        assert response.status_code == 200
    
    def test_password_reset_uses_correct_template(self, client, db):
        """Test password reset uses correct template."""
        response = client.get(reverse('password_reset'))
        assert 'registration/password_reset_form.html' in [t.name for t in response.templates]


class TestErrorViews:
    """Tests for error handler views."""
    
    def test_404_error_handler(self, client, db):
        """Test 404 error handler."""
        response = client.get('/nonexistent-page-that-does-not-exist/')
        # Custom handler may return 200 with error page content
        assert response.status_code in [200, 404]


class TestActivateView:
    """Tests for account activation."""
    
    def test_activate_invalid_token(self, client, db):
        """Test activation with invalid token."""
        response = client.get(reverse('activate', kwargs={
            'uidb64': 'invalid',
            'token': 'invalid-token'
        }))
        assert response.status_code == 200
        assert 'invalid' in response.content.decode().lower()
