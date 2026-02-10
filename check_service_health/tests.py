"""
Tests for check_service_health application.
"""
import pytest
from check_service_health.models import TestModel


class TestTestModel:
    """Tests for TestModel."""
    
    def test_testmodel_creation(self, db):
        """Test creating a TestModel instance."""
        instance = TestModel.objects.create(name='Test Service')
        assert instance.name == 'Test Service'
        assert instance.created_at is not None
    
    def test_testmodel_str(self, db):
        """Test TestModel string representation."""
        instance = TestModel.objects.create(name='Health Check')
        assert str(instance) == 'Health Check'
    
    def test_testmodel_max_length(self, db):
        """Test name field max length."""
        long_name = 'a' * 100
        instance = TestModel.objects.create(name=long_name)
        assert len(instance.name) == 100
    
    def test_testmodel_multiple_instances(self, db):
        """Test creating multiple TestModel instances."""
        TestModel.objects.create(name='Service 1')
        TestModel.objects.create(name='Service 2')
        TestModel.objects.create(name='Service 3')
        assert TestModel.objects.count() == 3

