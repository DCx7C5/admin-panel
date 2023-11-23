from datetime import datetime
import pytz

from django import template

from dashboard.models import HostManager

register = template.Library()


@register.simple_tag
def total_hosts():
    return HostManager.count()


@register.simple_tag(takes_context=True)
def current_datetime(context, format_string: str = '%Y-%m-%d %H:%M:%S') -> str:
    tz = context.get('timezone')
    if not tz:
        tz = 'UTC'
    return datetime.now(pytz.timezone(tz)).strftime(format_string)
