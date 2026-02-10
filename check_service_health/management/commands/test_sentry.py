# check_service_health/management/commands/test_sentry.py

from django.core.management.base import BaseCommand
from django.conf import settings
import sentry_sdk


class Command(BaseCommand):
    help = 'Test if Sentry error tracking is properly configured'

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write('Testing Sentry Configuration...\n')
            
            # Check if Sentry DSN is configured
            sentry_dsn = getattr(settings, 'SENTRY_DSH_URL', None)
            sentry_env = getattr(settings, 'SENTRY_ENVIRONMENT', 'unknown')
            
            if not sentry_dsn:
                self.stdout.write(self.style.WARNING('SENTRY_DSH_URL not configured in settings'))
                return
            
            self.stdout.write(f'Sentry DSN: {sentry_dsn[:50]}...')
            self.stdout.write(f'Sentry Environment: {sentry_env}')
            
            # Check if Sentry SDK is initialized
            client = sentry_sdk.get_client()
            
            if client.is_active():
                self.stdout.write(self.style.SUCCESS('✓ Sentry SDK is active and initialized'))
            else:
                self.stdout.write(self.style.ERROR('✗ Sentry SDK is not active'))
                return
            
            # Get the current hub to verify configuration
            hub = sentry_sdk.Hub.current
            
            if hub.client and hub.client.dsn:
                self.stdout.write(self.style.SUCCESS('✓ Sentry Hub is properly configured'))
            else:
                self.stdout.write(self.style.WARNING('⚠ Sentry Hub may not be fully configured'))
            
            # Test capture message (won't actually send in test mode)
            self.stdout.write('\nConfiguration check only - not sending test events to avoid noise.')
            self.stdout.write('To send a test event, use: sentry_sdk.capture_message("Test message")')
            
            # Check integrations
            integrations = client.options.get('integrations', [])
            if integrations:
                self.stdout.write(f'\nActive Integrations:')
                for integration in integrations:
                    integration_name = type(integration).__name__
                    self.stdout.write(f'  • {integration_name}')
            
            # Check sample rates
            traces_sample_rate = client.options.get('traces_sample_rate', 0)
            profiles_sample_rate = client.options.get('profiles_sample_rate', 0)
            
            self.stdout.write(f'\nSample Rates:')
            self.stdout.write(f'  • Traces: {traces_sample_rate * 100}%')
            self.stdout.write(f'  • Profiles: {profiles_sample_rate * 100}%')
            
            # Check release info
            release = client.options.get('release')
            if release:
                self.stdout.write(f'\nRelease: {release[:12]}...')
            
            self.stdout.write(self.style.SUCCESS('\n✓ Sentry health check passed'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error testing Sentry: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
