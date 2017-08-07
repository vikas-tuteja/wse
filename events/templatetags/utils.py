from django import template
register = template.Library()

@register.filter(name='slugify')
def slugify(obj):
    return obj.lower().replace(" ","-")
