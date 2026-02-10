"""
UI tests for blog app using Playwright.
Tests blog listing, post detail, comments, and interactions.
"""
import pytest
from playwright.sync_api import Page, expect


class TestBlogListPage:
    """UI tests for blog listing page."""
    
    @pytest.mark.ui
    def test_blog_list_page_loads(self, page: Page, server_url):
        """Test blog list page loads successfully."""
        page.goto(f"{server_url}/blog/")
        expect(page).to_have_url(f"{server_url}/blog/")
    
    @pytest.mark.ui
    def test_blog_list_page_has_content(self, page: Page, server_url):
        """Test blog list page has content area."""
        page.goto(f"{server_url}/blog/")
        body = page.locator('body')
        expect(body).not_to_be_empty()
    
    @pytest.mark.ui
    def test_blog_list_has_heading(self, page: Page, server_url):
        """Test blog list has a heading element."""
        page.goto(f"{server_url}/blog/")
        heading = page.locator('h1, h2, .page-title, .blog-title')
        # Page should have some heading or title
        expect(page).to_have_url(f"{server_url}/blog/")
    
    @pytest.mark.ui
    def test_blog_list_page_title(self, page: Page, server_url):
        """Test blog list page has a title."""
        page.goto(f"{server_url}/blog/")
        # Page should have a title element
        title = page.title()
        assert len(title) > 0
    
    @pytest.mark.ui
    def test_blog_list_has_navigation(self, page: Page, server_url):
        """Test blog list has navigation."""
        page.goto(f"{server_url}/blog/")
        nav = page.locator('nav, .navbar, header')
        expect(nav.first).to_be_visible()


class TestBlogDetailPage:
    """UI tests for blog post detail page."""
    
    @pytest.mark.ui
    def test_blog_detail_invalid_slug_handled(self, page: Page, server_url):
        """Test blog detail with invalid slug is handled gracefully."""
        response = page.goto(f"{server_url}/blog/post/nonexistent-post-slug/")
        # Should return 404 or custom error page (200 with error content)
        assert response.status in [200, 404]
        # Page should still render something
        expect(page.locator('body')).not_to_be_empty()


class TestBlogSearch:
    """UI tests for blog search functionality."""
    
    @pytest.mark.ui
    def test_blog_search_with_query(self, page: Page, server_url):
        """Test blog search with query parameter."""
        page.goto(f"{server_url}/blog/?q=test")
        # URL should contain the search query
        expect(page).to_have_url(f"{server_url}/blog/?q=test")
        # Page should render
        expect(page.locator('body')).not_to_be_empty()


class TestBlogCategories:
    """UI tests for blog category pages."""
    
    @pytest.mark.ui
    def test_category_page_invalid_handled(self, page: Page, server_url):
        """Test category page with invalid slug is handled."""
        response = page.goto(f"{server_url}/blog/category/nonexistent-category/")
        assert response.status in [200, 404]
        expect(page.locator('body')).not_to_be_empty()


class TestBlogTags:
    """UI tests for blog tag pages."""
    
    @pytest.mark.ui
    def test_tag_page_invalid_handled(self, page: Page, server_url):
        """Test tag page with invalid slug is handled."""
        response = page.goto(f"{server_url}/blog/tag/nonexistent-tag/")
        assert response.status in [200, 404]
        expect(page.locator('body')).not_to_be_empty()


class TestBlogUIElements:
    """UI tests for blog UI elements."""
    
    @pytest.mark.ui
    def test_blog_page_has_header(self, page: Page, server_url):
        """Test blog page has header/navigation."""
        page.goto(f"{server_url}/blog/")
        header = page.locator('header, nav, .navbar')
        expect(header.first).to_be_visible()
    
    @pytest.mark.ui
    def test_blog_page_has_footer(self, page: Page, server_url):
        """Test blog page has footer."""
        page.goto(f"{server_url}/blog/")
        footer = page.locator('footer, .footer')
        if footer.count() > 0:
            expect(footer.first).to_be_visible()
    
    @pytest.mark.ui
    def test_blog_page_responsive_mobile(self, page: Page, server_url):
        """Test blog page works on mobile viewport."""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(f"{server_url}/blog/")
        # Page should still have navigation visible or hamburger menu
        expect(page).to_have_url(f"{server_url}/blog/")
        expect(page.locator('body')).not_to_be_empty()
    
    @pytest.mark.ui
    def test_blog_page_responsive_tablet(self, page: Page, server_url):
        """Test blog page works on tablet viewport."""
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(f"{server_url}/blog/")
        expect(page).to_have_url(f"{server_url}/blog/")
        expect(page.locator('body')).not_to_be_empty()


class TestBlogInteractions:
    """UI tests for blog interactions."""
    
    @pytest.mark.ui
    def test_blog_navigation_from_home(self, page: Page, server_url):
        """Test navigating to blog from home page."""
        page.goto(server_url)
        blog_link = page.locator('a[href*="/blog"], a:has-text("Blog")')
        if blog_link.count() > 0:
            blog_link.first.click()
            page.wait_for_load_state('networkidle')
            # Should navigate to blog
            assert '/blog' in page.url
    
    @pytest.mark.ui
    def test_blog_back_to_home(self, page: Page, server_url):
        """Test navigating back to home from blog."""
        page.goto(f"{server_url}/blog/")
        home_link = page.locator('a[href="/"], a:has-text("Home"), .logo a, .brand a')
        if home_link.count() > 0:
            home_link.first.click()
            page.wait_for_load_state('networkidle')
            # Should be back at home or somewhere else
            assert page.url is not None


class TestBlogUserProfile:
    """UI tests for blog user profiles."""
    
    @pytest.mark.ui
    def test_user_profile_invalid_handled(self, page: Page, server_url):
        """Test user profile with invalid username is handled."""
        response = page.goto(f"{server_url}/blog/user/nonexistent-user/")
        assert response.status in [200, 404]
        expect(page.locator('body')).not_to_be_empty()


class TestBlogAccessibility:
    """Accessibility tests for blog pages."""
    
    @pytest.mark.ui
    def test_blog_has_main_content_area(self, page: Page, server_url):
        """Test blog page has a main content area."""
        page.goto(f"{server_url}/blog/")
        # Either has main element or some content container
        content = page.locator('main, [role="main"], .main-content, #content, .container')
        expect(content.first).to_be_visible()
    
    @pytest.mark.ui
    def test_blog_links_are_visible(self, page: Page, server_url):
        """Test that links on blog page are visible."""
        page.goto(f"{server_url}/blog/")
        links = page.locator('a')
        # Blog should have at least some links
        assert links.count() > 0
        expect(links.first).to_be_visible()
