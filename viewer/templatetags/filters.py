from django import template

register = template.Library()


@register.filter
def minutes_to_hours(value):
    if value:
        hours = int(value) // 60
        minutes = int(value) % 60
        return f"{hours:01d}h {minutes:02d}m"
    else:
        return f""


@register.filter
def to_int(value):
    return int(value)
