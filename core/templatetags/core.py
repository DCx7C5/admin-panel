from datetime import datetime

import pytz

from django import template

from django.template import Context

from asshatsuite import settings

register = template.Library()
User = settings.AUTH_USER_MODEL


@register.simple_tag(takes_context=True)
def bs5_js_url(ctx: Context):
    return ctx['']


@register.inclusion_tag(filename='lib/navbar/_navbar.html', takes_context=True)
def navbar(context: Context, mode, id, fixed):
    return {
        'mode': mode,
        'id': id,
        'fixed': 'fixed-top' if fixed is True else '',
        'user': context['user'],
    }


@register.inclusion_tag(filename='lib/scripts/_ajax_logout.html', takes_context=True)
def ajax_logout_javascript(context: Context, logout_url: str):
    return {'logout_url': logout_url, 'csrf_token': context.get('csrf_token')}


@register.simple_tag(takes_context=True)
def current_datetime(context, format_string: str = '%Y-%m-%d %H:%M:%S') -> str:
    tz = context.get('timezone')
    if not tz:
        tz = 'UTC'
    return datetime.now(pytz.timezone(tz)).strftime(format_string)
