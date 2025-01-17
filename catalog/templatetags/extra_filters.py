from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value) * float(arg)  # Ensures compatibility
    except (ValueError, TypeError):
        return 0  # Return 0 or an appropriate fallback value

from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Splits a string by the given delimiter.
    """
    return value.split(arg)

from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    """
    Adds a CSS class to a form field.
    Usage: {{ form.field_name|add_class:"form-control" }}
    """
    return value.as_widget(attrs={'class': arg})

