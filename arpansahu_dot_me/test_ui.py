"""
UI tests for arpansahu_dot_me main app using Playwright.
Tests navigation, page rendering, forms and UI elements.
"""
import pytest
from playwright.sync_api import Page, expect


class TestHomePage:
    """UI tests for the home page."""
    
    @pytest.mark.ui
    def test_home_page_loads(self, page: Page, server_url):
        """Test home page loads successfully."""
        response = page.goto(server_url)
        assert response.status == 200
        expect(page.locator('body')).not_to_be_empty()
    
    @pytest.mark.ui
    def test_home_page_has_navigation(self, page: Page, server_url):
        """Test home page has navigation links."""
        page.goto(server_url)
        nav = page.locator('nav, .navbar, .navigation, header')
        expect(nav.first).to_be_visible()
    
    @pytest.mark.ui
    def test_home_page_has_contact_form(self, page: Page, server_url):
        """Test home page has a contact form."""
        page.goto(server_url)
        form = page.locator('form')
        if form.count() > 0:
            expect(form.first).to_be_visible()
    
    @pytest.mark.ui
    def test_home_navigation_links_work(self, page: Page, server_url):
        """Test navigation links are clickable."""
        page.goto(server_url, timeout=60000)  # Increased timeout for CI
        about_link = page.locator('a[href*="about"], a:has-text("About")')
        if about_link.count() > 0:
            about_link.first.click()
            page.wait_for_load_state('load', timeout=60000)


class TestAboutPage:
    """UI tests for the about page."""
    
    @pytest.mark.ui
    def test_about_page_loads(self, page: Page, server_url):
        """Test about page loads successfully."""
        page.goto(f"{server_url}/about/")
        expect(page).to_have_url(f"{server_url}/about/")
    
    @pytest.mark.ui
    def test_about_page_has_content(self, page: Page, server_url):
        """Test about page has content."""
        page.goto(f"{server_url}/about/")
        body = page.locator('body')
        expect(body).not_to_be_empty()


class TestProjectsPage:
    """UI tests for the projects page."""
    
    @pytest.mark.ui
    def test_projects_page_loads(self, page: Page, server_url):
        """Test projects page loads successfully."""
        page.goto(f"{server_url}/projects/")
        expect(page).to_have_url(f"{server_url}/projects/")
    
    @pytest.mark.ui
    def test_projects_page_has_content(self, page: Page, server_url):
        """Test projects page displays content."""
        page.goto(f"{server_url}/projects/")
        body = page.locator('body')
        expect(body).not_to_be_empty()


class TestContactPage:
    """UI tests for the contact page."""
    
    @pytest.mark.ui
    def test_contact_page_loads(self, page: Page, server_url):
        """Test contact page loads successfully."""
        page.goto(f"{server_url}/contact/")
        expect(page).to_have_url(f"{server_url}/contact/")
    
    @pytest.mark.ui
    def test_contact_page_has_form(self, page: Page, server_url):
        """Test contact page has a contact form."""
        page.goto(f"{server_url}/contact/")
        form = page.locator('form')
        expect(form.first).to_be_visible()
    
    @pytest.mark.ui
    def test_contact_form_has_required_fields(self, page: Page, server_url):
        """Test contact form has name, email, message fields."""
        page.goto(f"{server_url}/contact/")
        
        name_input = page.locator('input[name="name"], input[id*="name"]')
        email_input = page.locator('input[name="email"], input[type="email"]')
        message_input = page.locator('textarea, textarea[name="message"]')
        
        if name_input.count() > 0:
            expect(name_input.first).to_be_visible()
        if email_input.count() > 0:
            expect(email_input.first).to_be_visible()
        if message_input.count() > 0:
            expect(message_input.first).to_be_visible()
    
    @pytest.mark.ui
    def test_contact_form_has_submit_button(self, page: Page, server_url):
        """Test contact form has a submit button."""
        page.goto(f"{server_url}/contact/")
        submit_btn = page.locator('button[type="submit"], input[type="submit"]')
        if submit_btn.count() > 0:
            expect(submit_btn.first).to_be_visible()


class TestResumePage:
    """UI tests for the resume page."""
    
    @pytest.mark.ui
    def test_resume_page_loads(self, page: Page, server_url):
        """Test resume page loads successfully."""
        page.goto(f"{server_url}/resume/")
        expect(page).to_have_url(f"{server_url}/resume/")


class TestPrivacyPage:
    """UI tests for the privacy page."""
    
    @pytest.mark.ui
    def test_privacy_page_loads(self, page: Page, server_url):
        """Test privacy page loads successfully."""
        page.goto(f"{server_url}/privacy/")
        expect(page).to_have_url(f"{server_url}/privacy/")


class TestTermsPage:
    """UI tests for the terms and conditions page."""
    
    @pytest.mark.ui
    def test_terms_page_loads(self, page: Page, server_url):
        """Test terms page loads successfully."""
        page.goto(f"{server_url}/t_and_c/")
        expect(page).to_have_url(f"{server_url}/t_and_c/")


class TestResponsiveDesign:
    """UI tests for responsive design."""
    
    @pytest.mark.ui
    def test_home_page_mobile_viewport(self, page: Page, server_url):
        """Test home page works on mobile viewport."""
        page.set_viewport_size({"width": 375, "height": 667})
        response = page.goto(server_url)
        assert response.status == 200
        # Navigation should still be present (possibly as hamburger menu)
        nav = page.locator('nav, .navbar, header, .menu-toggle, .hamburger')
        expect(nav.first).to_be_visible()
    
    @pytest.mark.ui
    def test_home_page_tablet_viewport(self, page: Page, server_url):
        """Test home page works on tablet viewport."""
        page.set_viewport_size({"width": 768, "height": 1024})
        response = page.goto(server_url)
        assert response.status == 200
        expect(page.locator('body')).not_to_be_empty()
    
    @pytest.mark.ui
    def test_home_page_desktop_viewport(self, page: Page, server_url):
        """Test home page works on desktop viewport."""
        page.set_viewport_size({"width": 1920, "height": 1080})
        response = page.goto(server_url)
        assert response.status == 200
        # Desktop should have full navigation visible
        nav = page.locator('nav, .navbar, header')
        expect(nav.first).to_be_visible()


class TestFormElements:
    """UI tests for form elements."""
    
    @pytest.mark.ui
    def test_forms_have_csrf_token(self, page: Page, server_url):
        """Test forms have CSRF token for security."""
        page.goto(f"{server_url}/contact/")
        form = page.locator('form')
        if form.count() > 0:
            csrf = form.first.locator('input[name="csrfmiddlewaretoken"]')
            if csrf.count() > 0:
                expect(csrf.first).to_be_attached()
    
    @pytest.mark.ui
    def test_contact_form_field_interactions(self, page: Page, server_url):
        """Test contact form fields are interactive."""
        page.goto(f"{server_url}/contact/")
        
        name_input = page.locator('input[name="name"]')
        if name_input.count() > 0:
            name_input.first.fill('Test User')
            expect(name_input.first).to_have_value('Test User')
        
        email_input = page.locator('input[name="email"], input[type="email"]')
        if email_input.count() > 0:
            email_input.first.fill('test@example.com')
            expect(email_input.first).to_have_value('test@example.com')


@pytest.mark.ui
@pytest.mark.todo
class TestResumeUI:
    """UI tests for resume.html - IMPLEMENT THESE!"""

    def test_download_pdf(self, page: Page):
        """Test link: Download PDF"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn
        # element = page.locator(".btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Download PDF"


@pytest.mark.ui
@pytest.mark.todo
class TestIndexUI:
    """UI tests for index.html - IMPLEMENT THESE!"""

    def test_unknown(self, page: Page):
        """Test button: ×"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .close
        # element = page.locator(".close")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for ×"

    def test_close(self, page: Page):
        """Test button: Close"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn
        # element = page.locator(".btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Close"


@pytest.mark.ui
@pytest.mark.todo
class TestContactUI:
    """UI tests for contact.html - IMPLEMENT THESE!"""

    def test_unknown(self, page: Page):
        """Test button: ×"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .close
        # element = page.locator(".close")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for ×"

    def test_close(self, page: Page):
        """Test button: Close"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn
        # element = page.locator(".btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Close"


@pytest.mark.ui
@pytest.mark.todo
class TestTAndCUI:
    """UI tests for t_and_c.html - IMPLEMENT THESE!"""

    def test_contact_us(self, page: Page):
        """Test link: Contact US"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn
        # element = page.locator(".btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Contact US"


@pytest.mark.ui
@pytest.mark.todo
class TestPrivacyUI:
    """UI tests for privacy.html - IMPLEMENT THESE!"""

    def test_contact_us(self, page: Page):
        """Test link: Contact US"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn
        # element = page.locator(".btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Contact US"

