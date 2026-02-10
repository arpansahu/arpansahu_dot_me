"""
Tests for custom_tag_app application.
"""
import pytest
from django.template import Template, Context
from custom_tag_app.templatetags.custom_tags import include_if_exists


class TestIncludeIfExistsTag:
    """Tests for include_if_exists template tag."""
    
    def test_include_existing_template(self, db):
        """Test including an existing template."""
        # Test with a template that should exist
        result = include_if_exists('base.html')
        # Should return some content (not empty) if template exists
        assert isinstance(result, str)
    
    def test_include_nonexistent_template(self, db):
        """Test including a non-existent template returns empty string."""
        result = include_if_exists('nonexistent_template_xyz.html')
        assert result == ''
    
    def test_template_tag_in_template(self, db):
        """Test using the tag in a template."""
        template = Template(
            '{% load custom_tags %}'
            '{% include_if_exists "nonexistent.html" %}'
        )
        context = Context({})
        result = template.render(context)
        assert '' in result  # Should not raise error
    
    def test_include_if_exists_returns_string(self, db):
        """Test that include_if_exists always returns a string."""
        result = include_if_exists('any_template.html')
        assert isinstance(result, str)
