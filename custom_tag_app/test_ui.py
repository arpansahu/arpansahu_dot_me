"""
UI tests for custom_tag_app using Playwright.
Tests template tags rendering in the UI.
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
class TestCustomTagsUI:
    """UI tests for custom template tags."""
    
    @pytest.mark.ui
    def test_include_if_exists_renders(self, page: Page, server_url):
        """Test include_if_exists tag renders on pages."""
        response = page.goto(server_url)
        assert response.status == 200
        # Custom tags render within templates - page should load without template errors
        expect(page.locator('body')).not_to_be_empty()
    
    @pytest.mark.ui
    def test_templates_load_without_error(self, page: Page, server_url):
        """Test templates using custom tags load correctly."""
        pages_to_test = ['/', '/about/', '/projects/', '/contact/']
        for page_url in pages_to_test:
            response = page.goto(f"{server_url}{page_url}")
            assert response.status == 200, f"Page {page_url} failed with status {response.status}"
            expect(page.locator('body')).not_to_be_empty()
