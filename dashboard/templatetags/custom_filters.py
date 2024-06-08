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

@register.filter
def num_range(start, end, step=1):
    return range(start, end, step)

@register.filter
def format_time(time_obj):
    return time_obj.strftime('%H:%M')
