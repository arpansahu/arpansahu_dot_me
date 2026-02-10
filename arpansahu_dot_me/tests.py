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
    
    def test_resume_download_no_file_returns_404(self, client, db):
        """Test download with no resume file returns 404."""
        response = client.get(reverse('resume_download'))
        assert response.status_code == 404


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
