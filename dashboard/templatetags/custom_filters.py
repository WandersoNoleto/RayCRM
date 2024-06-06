from django import template

register = template.Library()

@register.filter
def times(start, interval=1):
    hour = start
    minute = 0
    times_list = []
    while hour < 20:
        while minute < 60:
            times_list.append(f"{hour:02}:{minute:02}")
            minute += interval
        hour += 1
        minute = 0
    return times_list
