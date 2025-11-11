from django import template

register = template.Library()

@register.filter
def get_semester(value):
    """Extract semester number from subject value (e.g., 'mathematics_1' -> '1')"""
    if '_' in value:
        return value.split('_')[-1]
    return value

@register.filter
def split_subjects(value):
    """Split subjects string by comma and return list"""
    if value:
        return value.split(',')
    return []

@register.filter
def split(value, arg):
    """Split string by delimiter and return list"""
    if value:
        return value.split(arg)
    return []

@register.filter
def trim(value):
    """Trim whitespace from string"""
    if value:
        return value.strip()
    return value

@register.filter
def add_class(value, arg):
    """Add CSS class to form field widget"""
    return value.as_widget(attrs={'class': arg})
