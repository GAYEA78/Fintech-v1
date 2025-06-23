from django import template

register = template.Library()

@register.filter
def absolute(value):
    try:
        return abs(value)
    except:
        return value
