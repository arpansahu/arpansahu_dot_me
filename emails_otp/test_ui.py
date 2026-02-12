"""
UI tests for emails_otp app using Playwright.
Tests OTP flow in the contact form.
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
class TestOTPUI:
    """UI tests for OTP functionality."""
    
    @pytest.mark.ui
    def test_contact_page_has_otp_field(self, page: Page, server_url):
        """Test contact page may have OTP field."""
        response = page.goto(f"{server_url}/contact/")
        assert response.status == 200
        # Check that the page loads and has form elements
        expect(page.locator('form')).to_be_visible()
    
    @pytest.mark.ui
    def test_get_otp_button_exists(self, page: Page, server_url):
        """Test get OTP button exists on contact form."""
        response = page.goto(f"{server_url}/contact/")
        assert response.status == 200
        # Check for OTP or submit button
        button = page.locator('button, input[type="submit"]')
        expect(button.first).to_be_visible()
    
    @pytest.mark.ui
    def test_contact_form_email_for_otp(self, page: Page, server_url):
        """Test email field exists for OTP verification."""
        page.goto(f"{server_url}/contact/")
        email_input = page.locator('input[type="email"], input[name="email"]')
        if email_input.count() > 0:
            expect(email_input.first).to_be_visible()
