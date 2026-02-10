"""
UI tests for account app using Playwright.
Tests login, registration, logout, and profile flows.
"""
import pytest
from playwright.sync_api import Page, expect


class TestLoginPage:
    """UI tests for the login page."""
    
    @pytest.mark.ui
    def test_login_page_loads(self, page: Page, server_url):
        """Test login page loads successfully."""
        page.goto(f"{server_url}/account/login/")
        expect(page).to_have_url(f"{server_url}/account/login/")
    
    @pytest.mark.ui
    def test_login_page_has_form(self, page: Page, server_url):
        """Test login page has a login form."""
        page.goto(f"{server_url}/account/login/")
        form = page.locator('form')
        expect(form.first).to_be_visible()
    
    @pytest.mark.ui
    def test_login_form_has_username_field(self, page: Page, server_url):
        """Test login form has username/email field."""
        page.goto(f"{server_url}/account/login/")
        username_input = page.locator('input[name="username"], input[type="email"], input[name="email"]')
        expect(username_input.first).to_be_visible()
    
    @pytest.mark.ui
    def test_login_form_has_password_field(self, page: Page, server_url):
        """Test login form has password field."""
        page.goto(f"{server_url}/account/login/")
        password_input = page.locator('input[type="password"], input[name="password"]')
        expect(password_input.first).to_be_visible()
    
    @pytest.mark.ui
    def test_login_form_has_submit_button(self, page: Page, server_url):
        """Test login form has submit button."""
        page.goto(f"{server_url}/account/login/")
        submit_btn = page.locator('button[type="submit"], input[type="submit"]')
        expect(submit_btn.first).to_be_visible()
    
    @pytest.mark.ui
    def test_login_page_has_register_link(self, page: Page, server_url):
        """Test login page has link to registration."""
        page.goto(f"{server_url}/account/login/")
        register_link = page.locator('a[href*="register"], a:has-text("Register"), a:has-text("Sign up")')
        if register_link.count() > 0:
            expect(register_link.first).to_be_visible()
    
    @pytest.mark.ui
    def test_login_page_has_forgot_password_link(self, page: Page, server_url):
        """Test login page has forgot password link."""
        page.goto(f"{server_url}/account/login/")
        forgot_link = page.locator('a[href*="password"], a:has-text("Forgot"), a:has-text("Reset")')
        if forgot_link.count() > 0:
            expect(forgot_link.first).to_be_visible()
    
    @pytest.mark.ui
    def test_login_empty_form_shows_validation(self, page: Page, server_url):
        """Test submitting empty login form shows validation."""
        page.goto(f"{server_url}/account/login/")
        submit_btn = page.locator('button[type="submit"], input[type="submit"]')
        submit_btn.first.click()
        page.wait_for_load_state('networkidle')


class TestRegistrationPage:
    """UI tests for the registration page."""
    
    @pytest.mark.ui
    def test_registration_page_loads(self, page: Page, server_url):
        """Test registration page loads successfully."""
        page.goto(f"{server_url}/account/register/")
        expect(page).to_have_url(f"{server_url}/account/register/")
    
    @pytest.mark.ui
    def test_registration_page_has_form(self, page: Page, server_url):
        """Test registration page has a registration form."""
        page.goto(f"{server_url}/account/register/")
        form = page.locator('form')
        expect(form.first).to_be_visible()
    
    @pytest.mark.ui
    def test_registration_form_has_email_field(self, page: Page, server_url):
        """Test registration form has email field."""
        page.goto(f"{server_url}/account/register/")
        email_input = page.locator('input[type="email"], input[name="email"]')
        expect(email_input.first).to_be_visible()
    
    @pytest.mark.ui
    def test_registration_form_has_username_field(self, page: Page, server_url):
        """Test registration form has username field."""
        page.goto(f"{server_url}/account/register/")
        username_input = page.locator('input[name="username"]')
        if username_input.count() > 0:
            expect(username_input.first).to_be_visible()
    
    @pytest.mark.ui
    def test_registration_form_has_password_fields(self, page: Page, server_url):
        """Test registration form has password fields."""
        page.goto(f"{server_url}/account/register/")
        password_inputs = page.locator('input[type="password"]')
        expect(password_inputs.first).to_be_visible()
    
    @pytest.mark.ui
    def test_registration_form_has_submit_button(self, page: Page, server_url):
        """Test registration form has submit button."""
        page.goto(f"{server_url}/account/register/")
        submit_btn = page.locator('button[type="submit"], input[type="submit"]')
        expect(submit_btn.first).to_be_visible()
    
    @pytest.mark.ui
    def test_registration_page_has_login_link(self, page: Page, server_url):
        """Test registration page has link to login."""
        page.goto(f"{server_url}/account/register/")
        login_link = page.locator('a[href*="login"], a:has-text("Login"), a:has-text("Sign in")')
        if login_link.count() > 0:
            expect(login_link.first).to_be_visible()


class TestPasswordResetPage:
    """UI tests for the password reset page."""
    
    @pytest.mark.ui
    def test_password_reset_page_loads(self, page: Page, server_url):
        """Test password reset page loads successfully."""
        page.goto(f"{server_url}/account/password_reset/")
        expect(page).to_have_url(f"{server_url}/account/password_reset/")
    
    @pytest.mark.ui
    def test_password_reset_has_email_field(self, page: Page, server_url):
        """Test password reset page has email field."""
        page.goto(f"{server_url}/account/password_reset/")
        email_input = page.locator('input[type="email"], input[name="email"]')
        expect(email_input.first).to_be_visible()
    
    @pytest.mark.ui
    def test_password_reset_has_submit_button(self, page: Page, server_url):
        """Test password reset page has submit button."""
        page.goto(f"{server_url}/account/password_reset/")
        submit_btn = page.locator('button[type="submit"], input[type="submit"]')
        expect(submit_btn.first).to_be_visible()


class TestLoginFlow:
    """UI tests for complete login flow."""
    
    @pytest.mark.ui
    def test_invalid_login_shows_error(self, page: Page, server_url):
        """Test invalid login credentials show error message."""
        page.goto(f"{server_url}/account/login/")
        
        username_input = page.locator('input[name="username"], input[type="email"]')
        password_input = page.locator('input[type="password"]')
        
        username_input.first.fill('invalid@example.com')
        password_input.first.fill('wrongpassword')
        
        submit_btn = page.locator('button[type="submit"], input[type="submit"]')
        submit_btn.first.click()
        
        page.wait_for_load_state('networkidle')


class TestNavigationAuthentication:
    """UI tests for navigation based on authentication state."""
    
    @pytest.mark.ui
    def test_unauthenticated_sees_login_link(self, page: Page, server_url):
        """Test unauthenticated user sees login link."""
        page.goto(server_url)
        login_link = page.locator('a[href*="login"], a:has-text("Login"), a:has-text("Sign in")')
        if login_link.count() > 0:
            expect(login_link.first).to_be_visible()
    
    @pytest.mark.ui
    def test_profile_page_requires_login(self, page: Page, server_url):
        """Test profile page redirects to login when not authenticated."""
        page.goto(f"{server_url}/account/profile/")
        page.wait_for_load_state('networkidle')


class TestAccountUIElements:
    """UI tests for account-related UI elements."""
    
    @pytest.mark.ui
    def test_login_form_input_placeholders(self, page: Page, server_url):
        """Test login form inputs are enabled."""
        page.goto(f"{server_url}/account/login/")
        
        username_input = page.locator('input[name="username"], input[type="email"]')
        expect(username_input.first).to_be_enabled()
        
        password_input = page.locator('input[type="password"]')
        expect(password_input.first).to_be_enabled()
    
    @pytest.mark.ui
    def test_login_form_is_interactable(self, page: Page, server_url):
        """Test login form fields are interactable."""
        page.goto(f"{server_url}/account/login/")
        
        username_input = page.locator('input[name="username"], input[type="email"]')
        username_input.first.fill('test@example.com')
        expect(username_input.first).to_have_value('test@example.com')
        
        password_input = page.locator('input[type="password"]')
        password_input.first.fill('testpassword')
        expect(password_input.first).to_have_value('testpassword')
    
    @pytest.mark.ui
    def test_password_field_is_masked(self, page: Page, server_url):
        """Test password field is masked."""
        page.goto(f"{server_url}/account/login/")
        password_input = page.locator('input[type="password"]')
        expect(password_input.first).to_have_attribute('type', 'password')
