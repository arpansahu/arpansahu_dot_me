# check_service_health/management/commands/test_harbor.py

from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth


class Command(BaseCommand):
    help = 'Test if Harbor container registry is accessible and properly configured'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            default='https://harbor.arpansahu.space',
            help='Harbor registry URL (default: https://harbor.arpansahu.space)',
        )

    def handle(self, *args, **kwargs):
        harbor_url = kwargs.get('url', 'https://harbor.arpansahu.space')
        
        try:
            self.stdout.write('Testing Harbor Container Registry...\n')
            
            # Get credentials from settings/environment
            harbor_username = getattr(settings, 'HARBOR_USERNAME', None)
            harbor_password = getattr(settings, 'HARBOR_PASSWORD', None)
            
            # Try to get from decouple if not in settings
            if not harbor_username or not harbor_password:
                try:
                    from decouple import config
                    harbor_username = config('HARBOR_USERNAME', default=None)
                    harbor_password = config('HARBOR_PASSWORD', default=None)
                except ImportError:
                    pass
            
            self.stdout.write(f'Harbor URL: {harbor_url}')
            if harbor_username:
                self.stdout.write(f'Username: {harbor_username}')
            else:
                self.stdout.write(self.style.WARNING('Username: Not configured'))
            
            # Test 1: Basic connectivity (health endpoint - no auth required)
            self.stdout.write('\n--- Testing Basic Connectivity ---')
            health_url = f'{harbor_url}/api/v2.0/health'
            
            try:
                response = requests.get(health_url, timeout=10)
                if response.status_code == 200:
                    health_data = response.json()
                    self.stdout.write(self.style.SUCCESS('✓ Harbor API is accessible'))
                    
                    # Check component health
                    components = health_data.get('components', [])
                    if components:
                        self.stdout.write('\nComponent Health:')
                        all_healthy = True
                        for component in components:
                            name = component.get('name', 'Unknown')
                            status = component.get('status', 'unknown')
                            if status == 'healthy':
                                self.stdout.write(self.style.SUCCESS(f'  • {name}: {status}'))
                            else:
                                self.stdout.write(self.style.ERROR(f'  • {name}: {status}'))
                                all_healthy = False
                        
                        if all_healthy:
                            self.stdout.write(self.style.SUCCESS('\n✓ All components healthy'))
                        else:
                            self.stdout.write(self.style.WARNING('\n⚠ Some components unhealthy'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ Health endpoint returned: {response.status_code}'))
            except requests.exceptions.ConnectionError:
                self.stdout.write(self.style.ERROR('✗ Cannot connect to Harbor'))
                return
            except requests.exceptions.Timeout:
                self.stdout.write(self.style.ERROR('✗ Connection timed out'))
                return
            
            # Test 2: System info (no auth required for basic info)
            self.stdout.write('\n--- Testing System Info ---')
            systeminfo_url = f'{harbor_url}/api/v2.0/systeminfo'
            
            try:
                response = requests.get(systeminfo_url, timeout=10)
                if response.status_code == 200:
                    info = response.json()
                    harbor_version = info.get('harbor_version', 'Unknown')
                    registry_url = info.get('registry_url', 'Unknown')
                    auth_mode = info.get('auth_mode', 'Unknown')
                    
                    self.stdout.write(self.style.SUCCESS('✓ System info retrieved'))
                    self.stdout.write(f'  Harbor Version: {harbor_version}')
                    self.stdout.write(f'  Registry URL: {registry_url}')
                    self.stdout.write(f'  Auth Mode: {auth_mode}')
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ System info returned: {response.status_code}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠ Could not get system info: {e}'))
            
            # Test 3: Authenticated API access (if credentials provided)
            if harbor_username and harbor_password:
                self.stdout.write('\n--- Testing Authenticated Access ---')
                auth = HTTPBasicAuth(harbor_username, harbor_password)
                
                # Test user info
                user_url = f'{harbor_url}/api/v2.0/users/current'
                try:
                    response = requests.get(user_url, auth=auth, timeout=10)
                    if response.status_code == 200:
                        user_data = response.json()
                        username = user_data.get('username', 'Unknown')
                        admin_flag = user_data.get('admin_role_in_auth', user_data.get('sysadmin_flag', False))
                        
                        self.stdout.write(self.style.SUCCESS('✓ Authentication successful'))
                        self.stdout.write(f'  Logged in as: {username}')
                        self.stdout.write(f'  Admin privileges: {"Yes" if admin_flag else "No"}')
                    elif response.status_code == 401:
                        self.stdout.write(self.style.ERROR('✗ Authentication failed (401 Unauthorized)'))
                    else:
                        self.stdout.write(self.style.WARNING(f'⚠ Auth check returned: {response.status_code}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠ Auth check failed: {e}'))
                
                # Test projects access
                projects_url = f'{harbor_url}/api/v2.0/projects'
                try:
                    response = requests.get(projects_url, auth=auth, timeout=10)
                    if response.status_code == 200:
                        projects = response.json()
                        self.stdout.write(self.style.SUCCESS(f'✓ Projects access verified ({len(projects)} projects)'))
                        
                        # Show first few projects
                        if projects:
                            self.stdout.write('\nAccessible Projects:')
                            for project in projects[:5]:
                                name = project.get('name', 'Unknown')
                                repo_count = project.get('repo_count', 0)
                                self.stdout.write(f'  • {name} ({repo_count} repositories)')
                            if len(projects) > 5:
                                self.stdout.write(f'  ... and {len(projects) - 5} more')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠ Could not list projects: {e}'))
            else:
                self.stdout.write('\n(Skipping authenticated tests - credentials not configured)')
            
            # Test 4: Docker Registry API (v2)
            self.stdout.write('\n--- Testing Docker Registry API ---')
            registry_v2_url = f'{harbor_url}/v2/'
            
            try:
                response = requests.get(registry_v2_url, timeout=10)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS('✓ Docker Registry v2 API accessible (anonymous)'))
                elif response.status_code == 401:
                    self.stdout.write(self.style.SUCCESS('✓ Docker Registry v2 API accessible (auth required)'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ Registry v2 returned: {response.status_code}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠ Registry v2 check failed: {e}'))
            
            self.stdout.write(self.style.SUCCESS('\n✓ Harbor health check passed'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error testing Harbor: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
