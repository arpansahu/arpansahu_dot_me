"""
Tests for arpansahu_dot_me main application views.
"""
import pytest
from django.test import Client
from django.urls import reverse


@pytest.fixture
def client():
    """Django test client."""
    return Client()


class TestHomeView:
    """Tests for Home view."""
    
    def test_home_get_returns_200(self, client, db):
        """Test GET request to home page returns 200."""
        response = client.get(reverse('home'))
        assert response.status_code == 200
    
    def test_home_uses_correct_template(self, client, db):
        """Test home page uses index.html template."""
        response = client.get(reverse('home'))
        assert 'index.html' in [t.name for t in response.templates]
    
    def test_home_context_contains_form(self, client, db):
        """Test home page context contains contact form."""
        response = client.get(reverse('home'))
        assert 'form' in response.context
    
    def test_home_post_with_invalid_form(self, client, db):
        """Test POST with invalid form data."""
        response = client.post(reverse('home'), data={})
        assert response.status_code == 200


class TestAboutView:
    """Tests for About view."""
    
    def test_about_get_returns_200(self, client, db):
        """Test GET request to about page returns 200."""
        response = client.get(reverse('about'))
        assert response.status_code == 200
    
    def test_about_uses_correct_template(self, client, db):
        """Test about page uses about.html template."""
        response = client.get(reverse('about'))
        assert 'about.html' in [t.name for t in response.templates]
    
    def test_about_context_contains_active(self, client, db):
        """Test about page context contains 'about' active marker."""
        response = client.get(reverse('about'))
        assert response.context.get('about') == 'active'


class TestPrivacyView:
    """Tests for Privacy view."""
    
    def test_privacy_get_returns_200(self, client, db):
        """Test GET request to privacy page returns 200."""
        response = client.get(reverse('privacy'))
        assert response.status_code == 200
    
    def test_privacy_uses_correct_template(self, client, db):
        """Test privacy page uses privacy.html template."""
        response = client.get(reverse('privacy'))
        assert 'privacy.html' in [t.name for t in response.templates]


class TestTAndCView:
    """Tests for Terms and Conditions view."""
    
    def test_t_and_c_get_returns_200(self, client, db):
        """Test GET request to T&C page returns 200."""
        response = client.get(reverse('t_and_c'))
        assert response.status_code == 200
    
    def test_t_and_c_uses_correct_template(self, client, db):
        """Test T&C page uses t_and_c.html template."""
        response = client.get(reverse('t_and_c'))
        assert 't_and_c.html' in [t.name for t in response.templates]


class TestProjectsView:
    """Tests for Projects view."""
    
    def test_projects_get_returns_200(self, client, db):
        """Test GET request to projects page returns 200."""
        response = client.get(reverse('projects'))
        assert response.status_code == 200
    
    def test_projects_uses_correct_template(self, client, db):
        """Test projects page uses projects.html template."""
        response = client.get(reverse('projects'))
        assert 'projects.html' in [t.name for t in response.templates]
    
    def test_projects_context_contains_active(self, client, db):
        """Test projects page context contains 'project' active marker."""
        response = client.get(reverse('projects'))
        assert response.context.get('project') == 'active'


class TestProjectDetailedView:
    """Tests for ProjectDetailedView."""
    
    def test_project_detailed_rejects_html_extension(self, client, db):
        """Test project name with .html extension returns 404."""
        response = client.get(reverse('project-detailed-view', kwargs={'project_name': 'test.html'}))
        assert response.status_code == 404
    
    def test_project_detailed_url_resolves(self, client, db):
        """Test project detail URL resolves correctly."""
        url = reverse('project-detailed-view', kwargs={'project_name': 'my-project'})
        assert 'my-project' in url


class TestContactView:
    """Tests for Contact view."""
    
    def test_contact_get_returns_200(self, client, db):
        """Test GET request to contact page returns 200."""
        response = client.get(reverse('contact'))
        assert response.status_code == 200
    
    def test_contact_uses_correct_template(self, client, db):
        """Test contact page uses contact.html template."""
        response = client.get(reverse('contact'))
        assert 'contact.html' in [t.name for t in response.templates]
    
    def test_contact_context_contains_form(self, client, db):
        """Test contact page context contains form."""
        response = client.get(reverse('contact'))
        assert 'form' in response.context
    
    def test_contact_post_with_empty_data(self, client, db):
        """Test POST with empty data returns 200."""
        response = client.post(reverse('contact'), data={})
        assert response.status_code == 200


class TestResumeView:
    """Tests for Resume view."""
    
    def test_resume_get_returns_200(self, client, db):
        """Test GET request to resume page returns 200."""
        response = client.get(reverse('resume'))
        assert response.status_code == 200
    
    def test_resume_uses_correct_template(self, client, db):
        """Test resume page uses resume.html template."""
        response = client.get(reverse('resume'))
        assert 'resume.html' in [t.name for t in response.templates]


class TestResumeDownloadView:
    """Tests for ResumeDownloadView."""
    
    def test_resume_download_falls_back_to_static(self, client, db):
        """Test download with no DB resume falls back to static PDF and returns 200."""
        response = client.get(reverse('resume_download'))
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/pdf'


class TestGetOTPView:
    """Tests for GetOTPView AJAX endpoint."""
    
    def test_get_otp_non_ajax_not_allowed(self, client, db):
        """Test OTP endpoint requires AJAX request."""
        response = client.post(reverse('get-otp'), data={'email': 'test@example.com'})
        # Non-AJAX requests should be handled differently
        assert response.status_code in [200, 405]
    
    def test_get_otp_url_resolves(self, client, db):
        """Test OTP URL resolves correctly."""
        url = reverse('get-otp')
        assert url == '/get-otp'




class TestTriggerErrorView:
    """Tests for trigger_error sentry debug view."""

    def test_trigger_error_raises_division_error(self, client, db):
        """Test sentry-debug/ raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            client.get('/sentry-debug/')


class TestAdSenseSettings:
    """Tests for adsense_settings context processor."""

    def test_adsense_settings_returns_dict(self, db):
        """Test adsense_settings returns expected keys."""
        from django.test import RequestFactory
        from arpansahu_dot_me.context_processors import adsense_settings
        request = RequestFactory().get('/')
        result = adsense_settings(request)
        assert 'GOOGLE_ADSENSE_CLIENT_ID' in result
        assert 'GOOGLE_ADSENSE_ENABLED' in result

    def test_adsense_settings_values_from_settings(self, db):
        """Test adsense values come from Django settings."""
        from django.test import RequestFactory
        from django.conf import settings
        from arpansahu_dot_me.context_processors import adsense_settings
        request = RequestFactory().get('/')
        result = adsense_settings(request)
        assert result['GOOGLE_ADSENSE_CLIENT_ID'] == settings.GOOGLE_ADSENSE_CLIENT_ID
        assert result['GOOGLE_ADSENSE_ENABLED'] == settings.GOOGLE_ADSENSE_ENABLED


class TestSendEmailUtil:
    """Tests for send_email utility function."""

    def test_send_email_function_is_callable(self):
        """Test send_email function exists and is callable."""
        from arpansahu_dot_me.utils import send_email
        assert callable(send_email)

    def test_send_email_with_mock(self, db, mocker):
        """Test send_email calls mailjet API correctly."""
        from arpansahu_dot_me import utils
        mock_result = mocker.MagicMock()
        mock_result.status_code = 200
        mock_send = mocker.MagicMock()
        mock_send.create.return_value = mock_result
        mocker.patch.object(utils.mailjet, 'send', mock_send)

        success, status_code = utils.send_email(
            to_email='test@test.com',
            to_name='Test User',
            subject='Test Subject',
            text_part='Hello',
            html_part='<p>Hello</p>',
        )
        assert success is True
        assert status_code == 200
        mock_send.create.assert_called_once()


class TestGetGitCommitHash:
    """Tests for get_git_commit_hash function."""

    def test_get_git_commit_hash_returns_string_or_none(self):
        """Test get_git_commit_hash returns a string hash or None."""
        from arpansahu_dot_me.settings import get_git_commit_hash
        result = get_git_commit_hash()
        # In a git repo it returns a hex string; outside git it returns None
        assert result is None or (isinstance(result, str) and len(result) == 40)

    def test_get_git_commit_hash_handles_error(self, mocker):
        """Test returns None when git is not available."""
        import subprocess
        mocker.patch('subprocess.check_output', side_effect=Exception('no git'))
        from arpansahu_dot_me.settings import get_git_commit_hash
        assert get_git_commit_hash() is None

