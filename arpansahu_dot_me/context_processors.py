from django.conf import settings


def adsense_settings(request):
    """
    Make Google AdSense settings available in all templates
    """
    return {
        'GOOGLE_ADSENSE_CLIENT_ID': settings.GOOGLE_ADSENSE_CLIENT_ID,
        'GOOGLE_ADSENSE_ENABLED': settings.GOOGLE_ADSENSE_ENABLED,
    }
