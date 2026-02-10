# check_service_health/management/commands/test_storage.py

from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import uuid

# For Django 4.2+, storages is imported differently
try:
    from django.core.files.storage import storages
except ImportError:
    # Fallback for older Django versions
    storages = None


class Command(BaseCommand):
    help = 'Test if MinIO/S3 storage is working properly'

    def handle(self, *args, **kwargs):
        try:
            # Check if in DEBUG mode
            if settings.DEBUG:
                self.stdout.write(self.style.WARNING('DEBUG is True - MinIO configuration only applies when DEBUG=False'))
                self.stdout.write(self.style.WARNING('Set DEBUG=False in .env to test MinIO storage'))
                return
            
            # Check if using MinIO
            bucket_type = getattr(settings, 'BUCKET_TYPE', 'Unknown')
            self.stdout.write(f'Bucket Type: {bucket_type}')
            self.stdout.write(f'Bucket Name: {settings.AWS_STORAGE_BUCKET_NAME}')
            self.stdout.write(f'Endpoint URL: {settings.AWS_S3_ENDPOINT_URL}')
            
            # Check STORAGES configuration
            if hasattr(settings, 'STORAGES'):
                self.stdout.write(f'Storage Backend: {settings.STORAGES["default"]["BACKEND"]}')
            
            if storages:
                # Test default storage (public media)
                self.stdout.write('\n--- Testing Default Storage (Public Media) ---')
                self._test_storage('default', 'Default Storage')
                
                # Test private storage
                self.stdout.write('\n--- Testing Private Storage ---')
                self._test_storage('private', 'Private Storage')
                
                # Test static files storage
                self.stdout.write('\n--- Testing Static Files Storage ---')
                self._test_storage('staticfiles', 'Static Files Storage')
            else:
                # Use default_storage for older Django versions
                self.stdout.write('\n--- Testing Default Storage ---')
                self._test_default_storage()
            
            self.stdout.write(self.style.SUCCESS('\nStorage test completed successfully'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())

    def _test_storage(self, storage_name, display_name):
        """Test a specific storage backend"""
        try:
            # Get storage instance
            storage = storages[storage_name]
            
            # Generate unique filename
            test_filename = f'health-check-{uuid.uuid4()}.txt'
            test_content = f'Health check test file - {uuid.uuid4()}'
            
            # Test 1: Write file
            self.stdout.write(f'Writing test file: {test_filename}')
            file_path = storage.save(test_filename, ContentFile(test_content.encode()))
            self.stdout.write(self.style.SUCCESS(f'✓ File saved at: {file_path}'))
            
            # Test 2: Check file exists
            if storage.exists(file_path):
                self.stdout.write(self.style.SUCCESS(f'✓ File exists verification passed'))
            else:
                self.stdout.write(self.style.ERROR(f'✗ File exists check failed'))
                return
            
            # Test 3: Read file
            with storage.open(file_path, 'r') as f:
                content = f.read()
                if content == test_content:
                    self.stdout.write(self.style.SUCCESS(f'✓ File content verification passed'))
                else:
                    self.stdout.write(self.style.ERROR(f'✗ File content mismatch'))
                    return
            
            # Test 4: Get URL
            url = storage.url(file_path)
            self.stdout.write(f'File URL: {url}')
            
            # Test 5: Delete file
            storage.delete(file_path)
            self.stdout.write(self.style.SUCCESS(f'✓ File deleted successfully'))
            
            # Test 6: Verify deletion
            if not storage.exists(file_path):
                self.stdout.write(self.style.SUCCESS(f'✓ File deletion verified'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ File deletion verification failed'))
            
            self.stdout.write(self.style.SUCCESS(f'{display_name} test passed'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ {display_name} test failed: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())

    def _test_default_storage(self):
        """Test default_storage for older Django versions"""
        try:
            test_filename = f'health-check-{uuid.uuid4()}.txt'
            test_content = f'Health check test file - {uuid.uuid4()}'
            
            file_path = default_storage.save(test_filename, ContentFile(test_content.encode()))
            self.stdout.write(self.style.SUCCESS(f'✓ File saved at: {file_path}'))
            
            if default_storage.exists(file_path):
                self.stdout.write(self.style.SUCCESS(f'✓ File exists'))
            
            default_storage.delete(file_path)
            self.stdout.write(self.style.SUCCESS(f'✓ File deleted'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Storage test failed: {e}'))

