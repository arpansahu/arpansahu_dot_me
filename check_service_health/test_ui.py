"""
UI tests for check_service_health app using Playwright.
This app doesn't have UI views, so minimal UI tests.
"""
import pytest
from playwright.sync_api import Page, expect


class TestServiceHealthUI:
    """UI tests for service health checks."""
    
    @pytest.mark.ui
    def test_app_does_not_break_site(self, page: Page, server_url):
        """Test service health app doesn't break the main site."""
        response = page.goto(server_url)
        assert response.status == 200
        expect(page.locator('body')).not_to_be_empty()
