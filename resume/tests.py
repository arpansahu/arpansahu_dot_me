"""
Tests for resume application.
"""
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from resume.models import Resume


class TestResumeModel:
    """Tests for Resume model."""
    
    def test_resume_creation(self, db):
        """Test creating a Resume instance."""
        # Create a mock PDF file
        pdf_content = b'%PDF-1.4 mock pdf content'
        pdf_file = SimpleUploadedFile(
            name='test_resume.pdf',
            content=pdf_content,
            content_type='application/pdf'
        )
        resume = Resume.objects.create(file=pdf_file)
        assert resume.file is not None
        assert 'test_resume' in resume.file.name
    
    def test_resume_str(self, db):
        """Test Resume string representation."""
        pdf_content = b'%PDF-1.4 mock pdf content'
        pdf_file = SimpleUploadedFile(
            name='my_resume.pdf',
            content=pdf_content,
            content_type='application/pdf'
        )
        resume = Resume.objects.create(file=pdf_file)
        assert 'my_resume' in str(resume)
    
    def test_resume_upload_path(self, db):
        """Test resume file is uploaded to correct path."""
        pdf_content = b'%PDF-1.4 mock pdf content'
        pdf_file = SimpleUploadedFile(
            name='uploaded_resume.pdf',
            content=pdf_content,
            content_type='application/pdf'
        )
        resume = Resume.objects.create(file=pdf_file)
        # File should be in pdfs/ directory
        assert 'pdfs/' in resume.file.name
    
    def test_resume_ordering_by_id(self, db):
        """Test getting latest resume by id."""
        # Create multiple resumes
        for i in range(3):
            pdf_content = f'%PDF-1.4 mock pdf content {i}'.encode()
            pdf_file = SimpleUploadedFile(
                name=f'resume_{i}.pdf',
                content=pdf_content,
                content_type='application/pdf'
            )
            Resume.objects.create(file=pdf_file)
        
        latest = Resume.objects.order_by('id').last()
        assert latest is not None
        assert '2' in latest.file.name  # Last one should be resume_2
    
    def test_resume_file_field_required(self, db):
        """Test that file field requires a file."""
        with pytest.raises(Exception):
            # Creating resume without file should fail
            resume = Resume()
            resume.full_clean()
