# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-02-12
### Added
- **Social Authentication** via django-allauth (Google, GitHub, Twitter OAuth2, LinkedIn OpenID Connect)
- **Profile Management** page with social account connect/disconnect
- **Delete Account** functionality with admin protection
- **Blog Series Navigation** — sequence field, series dropdown, prev/next post cards
- **Blog Sidebar** with collapsible categories and sequenced posts (blog list page)
- **Comment Persistence** — author SET_NULL with `author_name_cache` field
- **Username Sanitization** — strips @domain from email-based usernames
- **Google AdSense** auto ads on blog pages only
- **Email Templates** for social welcome and account connection notifications

### Changed
- Renamed account app label from `account` to `user_account` (allauth compatibility)
- Blog detail page: removed sidebar, single-column 1100px layout
- Domain updated from arpansahu.me to arpansahu.space
- Contact form: fixed email overflow in sidebar

### Disabled
- Facebook OAuth (requires business verification)

### Security
- Removed hardcoded credentials from demo scripts
- Scrubbed passwords from git history

---

## [1.5.0] - 2025-06-05
### Added
- Service health check management commands (DB, cache, storage, Sentry, Mailjet, Harbor)
- Comprehensive test suite with pytest-django and Playwright
- Jenkins pipeline test stages with SKIP_TESTS parameter
- Rich dependency for django-test-enforcer

### Changed
- Replaced all CDN libraries with local versions
- Use in-memory SQLite for test database
- Fix Redis SSL: use CERT_NONE for self-signed certs

### Fixed
- Image tag extraction: use 'id' field to avoid greedy match
- Migration: remove indexes before removing fields (SQLite compatibility)
- Deploy: use sed instead of JsonSlurper to avoid NotSerializableException
- Reduce excessive padding in project detail hero sections

---

## [1.0.0] - 2024-06-27
### Added
- Initial release of the project
- User authentication module
- Blog with CKEditor rich text
- Projects portfolio page
- Contact form with OTP verification
- Resume page
- Admin panel with Django Jazzmin