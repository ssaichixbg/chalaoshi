from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def rate_center(value, length):
    value = str(value)
    length = int(length)
    value = value[:length]
    for i in range(0, length - len(value)):
        value = "&nbsp;%s&nbsp;" % value
    return mark_safe(value)