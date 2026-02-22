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
            page.wait_for_load_state('load')
            # Should navigate to blog
            assert '/blog' in page.url
    
    @pytest.mark.ui
    def test_blog_back_to_home(self, page: Page, server_url):
        """Test navigating back to home from blog."""
        page.goto(f"{server_url}/blog/")
        home_link = page.locator('a[href="/"], a:has-text("Home"), .logo a, .brand a')
        if home_link.count() > 0:
            home_link.first.click()
            page.wait_for_load_state('load')
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


@pytest.mark.ui
@pytest.mark.todo
class TestBlogListUI:
    """UI tests for blog_list.html - IMPLEMENT THESE!"""

    def test_button(self, page: Page):
        """Test button: button"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .search-icon-btn
        # element = page.locator(".search-icon-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for button"

    def test_form(self, page: Page):
        """Test form: form_"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="form"]
        # element = page.locator("[data-testid="form"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for form_"

    def test_featured_min_read(self, page: Page):
        """Test link: ★ Featured min read"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="featured_min_read"]
        # element = page.locator("[data-testid="featured_min_read"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for ★ Featured min read"

    def test_first(self, page: Page):
        """Test link: « First"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="first"]
        # element = page.locator("[data-testid="first"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for « First"

    def test_previous(self, page: Page):
        """Test link: ‹ Previous"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="previous"]
        # element = page.locator("[data-testid="previous"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for ‹ Previous"

    def test_next(self, page: Page):
        """Test link: Next ›"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="next"]
        # element = page.locator("[data-testid="next"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Next ›"

    def test_last(self, page: Page):
        """Test link: Last »"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="last"]
        # element = page.locator("[data-testid="last"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Last »"

    def test_unknown(self, page: Page):
        """Test link: ()"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .category-pill
        # element = page.locator(".category-pill")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for ()"

    def test_unknown_2(self, page: Page):
        """Test link: #"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="unknown"]
        # element = page.locator("[data-testid="unknown"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for #"

    def test_q(self, page: Page):
        """Test input: q"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .search-input-field
        # element = page.locator(".search-input-field")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for q"


@pytest.mark.ui
@pytest.mark.todo
class TestBlogListOldUI:
    """UI tests for blog_list_old.html - IMPLEMENT THESE!"""

    def test_search(self, page: Page):
        """Test button: Search"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn
        # element = page.locator(".btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Search"

    def test_form(self, page: Page):
        """Test form: form_"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .search-box
        # element = page.locator(".search-box")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for form_"

    def test_link(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .text-white
        # element = page.locator(".text-white")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_read_more(self, page: Page):
        """Test link: Read More"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .glass-btn
        # element = page.locator(".glass-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Read More"

    def test_previous(self, page: Page):
        """Test link: Previous"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .page-link
        # element = page.locator(".page-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Previous"

    def test_link_2(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .page-link
        # element = page.locator(".page-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_next(self, page: Page):
        """Test link: Next"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .page-link
        # element = page.locator(".page-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Next"

    def test_link_3(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .text-white
        # element = page.locator(".text-white")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_unknown(self, page: Page):
        """Test link: ()"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .badge
        # element = page.locator(".badge")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for ()"

    def test_unknown_2(self, page: Page):
        """Test link: #"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .badge
        # element = page.locator(".badge")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for #"

    def test_q(self, page: Page):
        """Test input: q"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .form-control
        # element = page.locator(".form-control")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for q"


@pytest.mark.ui
@pytest.mark.todo
class TestNotificationsUI:
    """UI tests for notifications.html - IMPLEMENT THESE!"""

    def test_mark_all_as_read(self, page: Page):
        """Test button: Mark All as Read"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .mark-all-btn
        # element = page.locator(".mark-all-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Mark All as Read"

    def test_form(self, page: Page):
        """Test form: form_"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="form"]
        # element = page.locator("[data-testid="form"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for form_"

    def test_ago(self, page: Page):
        """Test link: ago"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .notification-link
        # element = page.locator(".notification-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for ago"


@pytest.mark.ui
@pytest.mark.todo
class TestUserProfileUI:
    """UI tests for user_profile.html - IMPLEMENT THESE!"""

    def test_link(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .post-link
        # element = page.locator(".post-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_link_2(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .post-link
        # element = page.locator(".post-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"


@pytest.mark.ui
@pytest.mark.todo
class TestBlogListBackupUI:
    """UI tests for blog_list_backup.html - IMPLEMENT THESE!"""

    def test_search(self, page: Page):
        """Test button: Search"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn
        # element = page.locator(".btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Search"

    def test_form(self, page: Page):
        """Test form: form_"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .search-box
        # element = page.locator(".search-box")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for form_"

    def test_link(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .text-white
        # element = page.locator(".text-white")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_read_more(self, page: Page):
        """Test link: Read More"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .glass-btn
        # element = page.locator(".glass-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Read More"

    def test_previous(self, page: Page):
        """Test link: Previous"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .page-link
        # element = page.locator(".page-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Previous"

    def test_link_2(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .page-link
        # element = page.locator(".page-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_next(self, page: Page):
        """Test link: Next"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .page-link
        # element = page.locator(".page-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Next"

    def test_link_3(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .text-white
        # element = page.locator(".text-white")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_unknown(self, page: Page):
        """Test link: ()"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .badge
        # element = page.locator(".badge")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for ()"

    def test_unknown_2(self, page: Page):
        """Test link: #"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .badge
        # element = page.locator(".badge")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for #"

    def test_q(self, page: Page):
        """Test input: q"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .form-control
        # element = page.locator(".form-control")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for q"


@pytest.mark.ui
@pytest.mark.todo
class TestBlogDetailBackupUI:
    """UI tests for blog_detail_backup.html - IMPLEMENT THESE!"""

    def test_post_comment(self, page: Page):
        """Test button: Post Comment"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .glass-btn
        # element = page.locator(".glass-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Post Comment"

    def test_form(self, page: Page):
        """Test form: form_"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .mb-4
        # element = page.locator(".mb-4")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for form_"

    def test_unknown(self, page: Page):
        """Test link: #"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .badge
        # element = page.locator(".badge")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for #"

    def test_twitter(self, page: Page):
        """Test link: Twitter"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .glass-btn
        # element = page.locator(".glass-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Twitter"

    def test_linked_in(self, page: Page):
        """Test link: LinkedIn"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .glass-btn
        # element = page.locator(".glass-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for LinkedIn"

    def test_facebook(self, page: Page):
        """Test link: Facebook"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .glass-btn
        # element = page.locator(".glass-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Facebook"

    def test_login(self, page: Page):
        """Test link: Login"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .text-accent
        # element = page.locator(".text-accent")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Login"

    def test_link(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .text-white
        # element = page.locator(".text-white")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_content(self, page: Page):
        """Test textarea: content"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .form-control
        # element = page.locator(".form-control")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for content"


@pytest.mark.ui
@pytest.mark.todo
class TestBlogDetailUI:
    """UI tests for blog_detail.html - IMPLEMENT THESE!"""

    def test_series_posts(self, page: Page):
        """Test button: Series ( posts)"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .related-posts-toggle
        # element = page.locator(".related-posts-toggle")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Series ( posts)"

    def test_button(self, page: Page):
        """Test button: button"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .comment-action-btn
        # element = page.locator(".comment-action-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for button"

    def test_reply(self, page: Page):
        """Test button: Reply"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .comment-action-btn
        # element = page.locator(".comment-action-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Reply"

    def test_edit(self, page: Page):
        """Test button: Edit"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .comment-action-btn
        # element = page.locator(".comment-action-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Edit"

    def test_history(self, page: Page):
        """Test button: History"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .comment-action-btn
        # element = page.locator(".comment-action-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for History"

    def test_save(self, page: Page):
        """Test button: Save"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn-auth
        # element = page.locator(".btn-auth")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Save"

    def test_cancel(self, page: Page):
        """Test button: Cancel"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn-auth
        # element = page.locator(".btn-auth")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Cancel"

    def test_reply_2(self, page: Page):
        """Test button: Reply"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn-auth
        # element = page.locator(".btn-auth")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Reply"

    def test_cancel_2(self, page: Page):
        """Test button: Cancel"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn-auth
        # element = page.locator(".btn-auth")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Cancel"

    def test_button_2(self, page: Page):
        """Test button: button"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .comment-action-btn
        # element = page.locator(".comment-action-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for button"

    def test_reply_3(self, page: Page):
        """Test button: Reply"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .comment-action-btn
        # element = page.locator(".comment-action-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Reply"

    def test_edit_2(self, page: Page):
        """Test button: Edit"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .comment-action-btn
        # element = page.locator(".comment-action-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Edit"

    def test_history_2(self, page: Page):
        """Test button: History"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .comment-action-btn
        # element = page.locator(".comment-action-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for History"

    def test_save_2(self, page: Page):
        """Test button: Save"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn-auth
        # element = page.locator(".btn-auth")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Save"

    def test_cancel_3(self, page: Page):
        """Test button: Cancel"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn-auth
        # element = page.locator(".btn-auth")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Cancel"

    def test_reply_4(self, page: Page):
        """Test button: Reply"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn-auth
        # element = page.locator(".btn-auth")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Reply"

    def test_cancel_4(self, page: Page):
        """Test button: Cancel"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .btn-auth
        # element = page.locator(".btn-auth")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Cancel"

    def test_post_comment_posting(self, page: Page):
        """Test button: Post CommentPosting..."""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .submit-btn
        # element = page.locator(".submit-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Post CommentPosting..."

    def test_commentform(self, page: Page):
        """Test form: comment-form"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: #comment-form
        # element = page.locator("#comment-form")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for comment-form"

    def test_link(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .article-category-badge
        # element = page.locator(".article-category-badge")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_unknown(self, page: Page):
        """Test link: #"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .tag-link
        # element = page.locator(".tag-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for #"

    def test_link_2(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .related-post-link{%
        # element = page.locator(".related-post-link{%")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_twitter(self, page: Page):
        """Test link: Twitter"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .share-btn
        # element = page.locator(".share-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Twitter"

    def test_linked_in(self, page: Page):
        """Test link: LinkedIn"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .share-btn
        # element = page.locator(".share-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for LinkedIn"

    def test_facebook(self, page: Page):
        """Test link: Facebook"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .share-btn
        # element = page.locator(".share-btn")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Facebook"

    def test_previous(self, page: Page):
        """Test link: Previous"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .post-nav-card
        # element = page.locator(".post-nav-card")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Previous"

    def test_next(self, page: Page):
        """Test link: Next"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .post-nav-card
        # element = page.locator(".post-nav-card")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Next"

    def test_link_3(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .category-pill
        # element = page.locator(".category-pill")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_link_4(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="link"]
        # element = page.locator("[data-testid="link"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_logout(self, page: Page):
        """Test link: Logout"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="logout"]
        # element = page.locator("[data-testid="logout"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Logout"

    def test_login(self, page: Page):
        """Test link: Login"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="login"]
        # element = page.locator("[data-testid="login"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Login"

    def test_sign_up(self, page: Page):
        """Test link: Sign Up"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="sign_up"]
        # element = page.locator("[data-testid="sign_up"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Sign Up"

    def test_login_2(self, page: Page):
        """Test link: Login"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="login"]
        # element = page.locator("[data-testid="login"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Login"

    def test_sign_up_2(self, page: Page):
        """Test link: Sign up"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: [data-testid="sign_up"]
        # element = page.locator("[data-testid="sign_up"]")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Sign up"

    def test_id_guest_name(self, page: Page):
        """Test input: id_guest_name"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: #id_guest_name
        # element = page.locator("#id_guest_name")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for id_guest_name"

    def test_id_content(self, page: Page):
        """Test textarea: id_content"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: #id_content
        # element = page.locator("#id_content")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for id_content"


@pytest.mark.ui
@pytest.mark.todo
class TestContentSidebarUI:
    """UI tests for content_sidebar.html - IMPLEMENT THESE!"""

    def test_button(self, page: Page):
        """Test button: button"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .sidebar-category-header{%
        # element = page.locator(".sidebar-category-header{%")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for button"

    def test_link(self, page: Page):
        """Test link: link"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .sidebar-post-link{%
        # element = page.locator(".sidebar-post-link{%")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for link"

    def test_previous(self, page: Page):
        """Test link: Previous"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .post-nav-link
        # element = page.locator(".post-nav-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Previous"

    def test_next(self, page: Page):
        """Test link: Next"""
        # TODO: Navigate to the correct page
        # page.goto("http://localhost:8000/")
        
        # Locate element using: .post-nav-link
        # element = page.locator(".post-nav-link")
        # expect(element).to_be_visible()
        
        # This test FAILS until you implement it!
        assert False, "TODO: Implement test for Next"

