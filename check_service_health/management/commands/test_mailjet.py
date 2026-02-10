# check_service_health/management/commands/test_mailjet.py

from django.core.management.base import BaseCommand
from django.conf import settings
from mailjet_rest import Client


class Command(BaseCommand):
    help = 'Test if Mailjet email service is properly configured and accessible'

    def add_arguments(self, parser):
        parser.add_argument(
            '--send-test',
            action='store_true',
            help='Send an actual test email (requires MY_EMAIL_ADDRESS to be set)',
        )

    def handle(self, *args, **kwargs):
        send_test = kwargs.get('send_test', False)
        
        try:
            self.stdout.write('Testing Mailjet Configuration...\n')
            
            # Check if Mailjet credentials are configured
            api_key = getattr(settings, 'MAIL_JET_API_KEY', None)
            api_secret = getattr(settings, 'MAIL_JET_API_SECRET', None)
            sender_email = getattr(settings, 'MAIL_JET_EMAIL_ADDRESS', None)
            my_email = getattr(settings, 'MY_EMAIL_ADDRESS', None)
            
            if not api_key:
                self.stdout.write(self.style.ERROR('✗ MAIL_JET_API_KEY not configured'))
                return
            
            if not api_secret:
                self.stdout.write(self.style.ERROR('✗ MAIL_JET_API_SECRET not configured'))
                return
                
            self.stdout.write(f'API Key: {api_key[:8]}...{api_key[-4:]}')
            self.stdout.write(f'Sender Email: {sender_email}')
            self.stdout.write(f'Admin Email: {my_email}')
            
            # Initialize Mailjet client
            self.stdout.write('\nInitializing Mailjet client...')
            mailjet = Client(auth=(api_key, api_secret), version='v3.1')
            self.stdout.write(self.style.SUCCESS('✓ Mailjet client initialized'))
            
            # Test API connectivity by getting sender addresses
            self.stdout.write('\nTesting API connectivity...')
            
            # Use v3 API to list senders (verifies credentials)
            mailjet_v3 = Client(auth=(api_key, api_secret), version='v3')
            
            try:
                # Get account profile to verify API access
                result = mailjet_v3.sender.get()
                
                if result.status_code == 200:
                    self.stdout.write(self.style.SUCCESS('✓ API credentials validated'))
                    
                    senders = result.json().get('Data', [])
                    if senders:
                        self.stdout.write(f'\nConfigured Sender Addresses ({len(senders)}):')
                        for sender in senders[:5]:  # Show first 5 senders
                            email = sender.get('Email', 'N/A')
                            name = sender.get('Name', 'N/A')
                            status = sender.get('Status', 'N/A')
                            self.stdout.write(f'  • {name} <{email}> - Status: {status}')
                        if len(senders) > 5:
                            self.stdout.write(f'  ... and {len(senders) - 5} more')
                elif result.status_code == 401:
                    self.stdout.write(self.style.ERROR('✗ Invalid API credentials (401 Unauthorized)'))
                    return
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ Unexpected response: {result.status_code}'))
                    
            except Exception as api_error:
                self.stdout.write(self.style.WARNING(f'⚠ Could not verify senders: {api_error}'))
                self.stdout.write('Attempting basic connectivity check...')
            
            # Check API statistics (another way to verify connectivity)
            try:
                stats_result = mailjet_v3.statcounters.get()
                if stats_result.status_code == 200:
                    self.stdout.write(self.style.SUCCESS('✓ API statistics endpoint accessible'))
                    stats = stats_result.json().get('Data', [{}])
                    if stats:
                        total = stats[0] if isinstance(stats, list) and stats else stats
                        if isinstance(total, dict):
                            sent = total.get('MessageSentCount', 'N/A')
                            self.stdout.write(f'  Total messages sent: {sent}')
            except Exception:
                pass  # Statistics endpoint is optional
            
            # Send test email if requested
            if send_test:
                if not my_email:
                    self.stdout.write(self.style.WARNING('\n⚠ Cannot send test email: MY_EMAIL_ADDRESS not configured'))
                else:
                    self.stdout.write(f'\nSending test email to {my_email}...')
                    
                    from datetime import datetime
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    data = {
                        'Messages': [
                            {
                                "From": {
                                    "Email": sender_email or "admin@arpansahu.space",
                                    "Name": "Health Check"
                                },
                                "To": [
                                    {
                                        "Email": my_email,
                                        "Name": "Admin"
                                    }
                                ],
                                "Subject": f"Health Check Test - {timestamp}",
                                "TextPart": f"This is a test email from arpansahu.space health check system.\n\nTimestamp: {timestamp}",
                                "HTMLPart": f"<h3>Health Check Test</h3><p>This is a test email from <strong>arpansahu.space</strong> health check system.</p><p>Timestamp: {timestamp}</p>",
                                "CustomID": f"health_check_{timestamp.replace(' ', '_').replace(':', '-')}"
                            }
                        ]
                    }
                    
                    result = mailjet.send.create(data=data)
                    
                    if result.status_code == 200:
                        self.stdout.write(self.style.SUCCESS(f'✓ Test email sent successfully to {my_email}'))
                        response = result.json()
                        messages = response.get('Messages', [])
                        if messages:
                            msg_status = messages[0].get('Status', 'unknown')
                            self.stdout.write(f'  Status: {msg_status}')
                    else:
                        self.stdout.write(self.style.ERROR(f'✗ Failed to send test email: {result.status_code}'))
                        self.stdout.write(f'  Response: {result.json()}')
            else:
                self.stdout.write('\n(Use --send-test flag to send an actual test email)')
            
            self.stdout.write(self.style.SUCCESS('\n✓ Mailjet health check passed'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error testing Mailjet: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
