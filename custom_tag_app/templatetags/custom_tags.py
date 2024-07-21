from django import template
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

register = template.Library()


@register.simple_tag
def include_if_exists(template_name):
    try:
        get_template(template_name)
        return template.loader.render_to_string(template_name)
    except TemplateDoesNotExist:
        return ''