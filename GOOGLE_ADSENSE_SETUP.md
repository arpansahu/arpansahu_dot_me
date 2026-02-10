# Google AdSense Integration Guide

This guide explains how to integrate Google AdSense ads into your blog, similar to WordPress websites.

## Overview

The blog now supports Google AdSense integration with ads displayed in:
- **Between blog posts** in the list view (after every 3rd post)
- **Sidebar panels** in blog detail view (multiple ad slots)
- **In-article ads** can be manually added to content

## Setup Steps

### 1. Get Your AdSense Account

1. Go to [Google AdSense](https://www.google.com/adsense/)
2. Sign up or log in with your Google account
3. Complete the account setup and verification process
4. Add your website domain for approval

### 2. Get Your Publisher ID

1. Once approved, go to your AdSense dashboard
2. Navigate to **Account** → **Account Information**
3. Find your **Publisher ID** (format: `ca-pub-XXXXXXXXXXXXXXXX`)
4. Copy this ID

### 3. Configure Your Application

Add these variables to your `.env` file:

```bash
# Google AdSense Configuration
GOOGLE_ADSENSE_CLIENT_ID=ca-pub-XXXXXXXXXXXXXXXX
GOOGLE_ADSENSE_ENABLED=True
```

**Important:** Replace `ca-pub-XXXXXXXXXXXXXXXX` with your actual Publisher ID

### 4. Create Ad Units (Optional)

For better control and performance tracking:

1. Go to **Ads** → **Overview** in AdSense dashboard
2. Click **By ad unit** → **Display ads**
3. Create ad units for:
   - Blog List Display Ad
   - Sidebar Ad (create 2-3 for multiple slots)
   - In-Article Ad
4. Copy the `data-ad-slot` values

5. Update the ad templates in `templates/ads/` with your slot IDs:
   - `display_ad.html` - for blog list
   - `sidebar_ad.html` - for sidebar
   - `in_article_ad.html` - for in-content ads

Replace the empty `data-ad-slot=""` with your actual slot IDs like `data-ad-slot="1234567890"`

## Ad Placements

### Blog List Page (`/blog/`)
- **Display ads** appear after every 3rd blog post
- Responsive and full-width
- Automatically hidden if AdSense is disabled

### Blog Detail Page (`/blog/<slug>/`)
- **Sidebar layout** with multiple ad slots:
  - Top sidebar ad (above related posts)
  - Middle sidebar ad (below related posts)
  - Categories widget between ads
- **Sticky sidebar** - ads stay visible while scrolling
- Responsive design - sidebar stacks below content on mobile

### Manual In-Article Ads
To add ads within blog post content:

1. Edit your blog post in CKEditor
2. Switch to **Source** mode
3. Add this code where you want the ad:
```html
{% include 'ads/in_article_ad.html' %}
```

## Ad Template Files

All ad templates are in `templates/ads/`:

- **`display_ad.html`** - Responsive display ad for blog list
- **`sidebar_ad.html`** - Vertical ad for sidebar
- **`in_article_ad.html`** - In-article ad for content

Each template:
- Checks if AdSense is enabled
- Uses your Publisher ID from settings
- Includes async loading for performance
- Responsive and mobile-friendly

## Testing

### Development Testing
1. Set `GOOGLE_ADSENSE_ENABLED=True` in your `.env`
2. Add your `GOOGLE_ADSENSE_CLIENT_ID`
3. Visit `/blog/` and `/blog/<any-post>/`
4. You should see placeholder ads (may show as blank during initial approval)

### Production
1. Ensure your domain is verified in AdSense
2. Wait for Google to crawl and approve your site (can take 24-48 hours)
3. Ads will start showing once approved

## Customization

### Styling Ad Containers

Ads are wrapped in containers with classes:
- `.adsense-container` - for display ads in blog list
- `.adsense-sidebar` - for sidebar ads
- `.adsense-in-article` - for in-article ads

You can add custom CSS in your templates to style these containers.

### Changing Ad Frequency

To change how often ads appear in blog list, edit `templates/blog/blog_list.html`:

```django
{# Change the divisor to show ads more/less frequently #}
{% if forloop.counter0|divisibleby:3 and forloop.counter0 > 0 %}
    {% include 'ads/display_ad.html' %}
{% endif %}
```

- `divisibleby:3` - shows ad every 3 posts
- Change to `divisibleby:5` for every 5 posts, etc.

### Adding More Sidebar Ads

In `templates/blog/blog_detail.html`, you can add more ad widgets:

```django
<div class="sidebar-widget">
    <h3 class="sidebar-widget-title">Advertisement</h3>
    {% include 'ads/sidebar_ad.html' %}
</div>
```

## Disabling Ads

To temporarily disable all ads:

```bash
GOOGLE_ADSENSE_ENABLED=False
```

Or remove the `GOOGLE_ADSENSE_CLIENT_ID` value.

## Performance Optimization

The implementation uses:
- **Async loading** - ads don't block page rendering
- **Lazy loading** - ads load as user scrolls
- **Responsive sizing** - `data-full-width-responsive="true"`
- **Auto format** - Google optimizes ad sizes automatically

## Compliance

### Required Pages
Google AdSense requires these pages (already in your site):
- Privacy Policy (`/privacy/`)
- Terms and Conditions (`/t_and_c/`)

### GDPR/Cookie Consent
If you have European users, consider adding a cookie consent banner. Google provides this through AdSense settings.

## Troubleshooting

### Ads Not Showing
1. Check `GOOGLE_ADSENSE_ENABLED=True` in `.env`
2. Verify `GOOGLE_ADSENSE_CLIENT_ID` is correct
3. Ensure domain is approved in AdSense dashboard
4. Check browser console for JavaScript errors
5. Wait 24-48 hours after setup for ads to appear

### Blank Ad Spaces
- Normal during initial approval period
- AdSense may not have ads for your content yet
- Low traffic sites may have limited ad inventory

### Ad Placement Issues
- Check browser developer tools for layout issues
- Verify templates are included correctly
- Ensure no CSS conflicts with `.adsense-*` classes

## Best Practices

1. **Content Quality** - Write high-quality, original content
2. **User Experience** - Don't overwhelm with too many ads
3. **Mobile Optimization** - Test on mobile devices
4. **Page Speed** - Monitor site performance
5. **AdSense Policies** - Follow Google's program policies
6. **Natural Placement** - Ads should blend with content layout

## Resources

- [Google AdSense Help](https://support.google.com/adsense/)
- [AdSense Program Policies](https://support.google.com/adsense/answer/48182)
- [Ad Implementation Guide](https://support.google.com/adsense/answer/9274025)

## Support

For issues with:
- **AdSense approval** - Contact Google AdSense support
- **Technical integration** - Check application logs and browser console
- **Ad performance** - Use AdSense dashboard analytics
