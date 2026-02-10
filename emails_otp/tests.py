"""
Tests for emails_otp application.
"""
import pytest
from django.utils import timezone
from datetime import date
from emails_otp.models import EmailsOtpRecord


class TestEmailsOtpRecordModel:
    """Tests for EmailsOtpRecord model."""
    
    def test_emailsotprecord_creation(self, db):
        """Test creating an EmailsOtpRecord instance."""
        record = EmailsOtpRecord.objects.create(
            email='test@example.com'
        )
        assert record.email == 'test@example.com'
        assert record.count == 1
        # Date can be datetime or date depending on model definition
        assert record.date is not None
    
    def test_emailsotprecord_default_count(self, db):
        """Test default count is 1."""
        record = EmailsOtpRecord.objects.create(email='default@example.com')
        assert record.count == 1
    
    def test_emailsotprecord_increment_count(self, db):
        """Test incrementing OTP count."""
        record = EmailsOtpRecord.objects.create(email='increment@example.com')
        record.count += 1
        record.save()
        record.refresh_from_db()
        assert record.count == 2
    
    def test_emailsotprecord_unique_together(self, db):
        """Test email + date unique constraint."""
        EmailsOtpRecord.objects.create(
            email='unique@example.com',
            date=date.today()
        )
        with pytest.raises(Exception):  # IntegrityError
            EmailsOtpRecord.objects.create(
                email='unique@example.com',
                date=date.today()
            )
    
    def test_emailsotprecord_same_email_different_dates(self, db):
        """Test same email can exist for different dates."""
        from datetime import timedelta
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        EmailsOtpRecord.objects.create(email='multi@example.com', date=today)
        record2 = EmailsOtpRecord.objects.create(email='multi@example.com', date=yesterday)
        
        assert EmailsOtpRecord.objects.filter(email='multi@example.com').count() == 2
    
    def test_emailsotprecord_max_count_tracking(self, db):
        """Test tracking OTP count up to maximum (5 per day)."""
        record = EmailsOtpRecord.objects.create(email='maxcount@example.com')
        
        # Simulate 5 OTP requests
        for i in range(5):
            record.count = i + 1
            record.save()
        
        record.refresh_from_db()
        assert record.count == 5
    
    def test_emailsotprecord_filter_by_date(self, db):
        """Test filtering records by date."""
        today = date.today()
        EmailsOtpRecord.objects.create(email='filter@example.com', date=today)
        
        records = EmailsOtpRecord.objects.filter(email='filter@example.com', date=today)
        assert records.count() == 1
    
    def test_emailsotprecord_filter_nonexistent(self, db):
        """Test filtering returns empty for nonexistent records."""
        records = EmailsOtpRecord.objects.filter(
            email='nonexistent@example.com',
            date=date.today()
        )
        assert records.count() == 0
