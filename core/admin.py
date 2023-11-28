from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session

from core.models import Host, Endpoint


@admin.register(Session)
class SessionAdmin(ModelAdmin):
    list_display = ['session_key', 'session_data', 'expire_date']


@admin.register(LogEntry)
class AdminLogAdmin(ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'change_message', 'is_addition', 'is_change', 'is_deletion')
    list_filter = ['action_time', 'user', 'content_type']
    ordering = ('-action_time',)


@admin.register(Endpoint)
class EndpointAdmin(ModelAdmin):
    list_display = ('id', 'name', 'segment', 'parent_id')


@admin.register(Host)
class HostAdmin(ModelAdmin):
    list_display = ('id', 'name', 'address', 'remote', 'created', 'updated')

