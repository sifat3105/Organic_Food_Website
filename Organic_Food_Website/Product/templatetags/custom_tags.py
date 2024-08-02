from django import template

register = template.Library()

@register.simple_tag
def calculate_percentage(rating):
    return rating * 20
