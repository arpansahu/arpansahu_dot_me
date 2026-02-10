import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    """
    Convert markdown text to HTML
    """
    return mark_safe(md.markdown(
        text,
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br',
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
                'linenums': False,
            }
        }
    ))


@register.filter
def reading_time(text):
    """Calculate reading time"""
    word_count = len(text.split())
    minutes = word_count / 200
    return max(1, round(minutes))
