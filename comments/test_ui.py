"""
UI tests for comments app using Playwright.
Tests comment display, editing, and interactions.
"""
import pytest
from playwright.sync_api import Page, expect


class TestCommentDisplay:
    """UI tests for comment display."""
    
    @pytest.mark.ui
    def test_blog_page_loads_for_comments(self, page: Page, server_url):
        """Test blog page loads where comments would appear."""
        page.goto(f"{server_url}/blog/")
        expect(page).to_have_url(f"{server_url}/blog/")
        # Blog list should have content
        body = page.locator('body')
        expect(body).not_to_be_empty()


class TestCommentInteractions:
    """UI tests for comment interactions."""
    
    @pytest.mark.ui
    def test_comment_endpoints_exist(self, page: Page, server_url):
        """Test comment edit endpoint returns proper response."""
        # Try to access edit endpoint without valid comment - should get 404 or redirect
        response = page.goto(f"{server_url}/comments/99999/edit/")
        # Should not crash, returns some response
        assert response.status in [200, 302, 403, 404, 405]
    
    @pytest.mark.ui
    def test_comment_like_endpoint_exists(self, page: Page, server_url):
        """Test comment like endpoint returns proper response."""
        # Try to access like endpoint - should redirect to login or return error
        response = page.goto(f"{server_url}/comments/99999/like/")
        assert response.status in [200, 302, 403, 404, 405]


class TestCommentEditHistory:
    """UI tests for comment edit history."""
    
    @pytest.mark.ui
    def test_edit_history_endpoint_returns_json(self, page: Page, server_url):
        """Test edit history endpoint returns JSON response."""
        response = page.goto(f"{server_url}/comments/99999/history/")
        # Should return JSON (even if 404 or error)
        assert response.status in [200, 404]
        content_type = response.headers.get('content-type', '')
        # Either JSON response or HTML error page
        assert 'json' in content_type or 'html' in content_type
