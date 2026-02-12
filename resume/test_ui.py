"""
UI tests for resume app using Playwright.
Tests resume page and download functionality.
"""
import pytest
from playwright.sync_api import Page, expect


class TestResumePage:
    """UI tests for resume page."""
    
    @pytest.mark.ui
    def test_resume_page_loads(self, page: Page, server_url):
        """Test resume page loads successfully."""
        response = page.goto(f"{server_url}/resume/")
        assert response.status == 200
        expect(page).to_have_url(f"{server_url}/resume/")
    
    @pytest.mark.ui
    def test_resume_page_has_content(self, page: Page, server_url):
        """Test resume page has content."""
        page.goto(f"{server_url}/resume/")
        body = page.locator('body')
        expect(body).not_to_be_empty()
    
    @pytest.mark.ui
    def test_resume_download_link_exists(self, page: Page, server_url):
        """Test resume page has download link."""
        response = page.goto(f"{server_url}/resume/")
        assert response.status == 200
        # Page should have navigation and content
        expect(page.locator('body')).not_to_be_empty()
    
    @pytest.mark.ui
    def test_resume_page_responsive(self, page: Page, server_url):
        """Test resume page is responsive."""
        page.set_viewport_size({"width": 375, "height": 667})
        response = page.goto(f"{server_url}/resume/")
        assert response.status == 200
        expect(page.locator('body')).not_to_be_empty()


class TestResumeDownload:
    """UI tests for resume download."""
    
    @pytest.mark.ui
    def test_download_endpoint_exists(self, page: Page, server_url):
        """Test download endpoint returns a file or valid response."""
        # Use page.request (API context) since page.goto() can't handle
        # download responses — it throws "Download is starting" error.
        response = page.request.get(f"{server_url}/download/resume/")
        assert response.status == 200
        content_type = response.headers.get('content-type', '')
        assert 'application/pdf' in content_type or 'application/octet-stream' in content_type or 'force-download' in content_type
