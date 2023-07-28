from django import template

register = template.Library()


@register.filter
def minutes_to_hours(value):
    hours = value // 60
    minutes = value % 60
    return f"{hours:01d}h {minutes:02d}m"
