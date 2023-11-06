from django import template
import json

register = template.Library()

@register.filter
def json_filter(value):
    return json.dumps(value)
