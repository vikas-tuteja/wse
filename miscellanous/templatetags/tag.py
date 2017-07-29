from django import template
register = template.Library()

@register.filter(name='islist')
def islist(obj):
    if isinstance(obj, list):
        return True

    return False
