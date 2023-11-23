from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session

from dashboard.models import Host, MenuItem


@admin.register(Session)
class SessionAdmin(ModelAdmin):
    list_display = ['session_key', 'session_data', 'expire_date']


@admin.register(LogEntry)
class AdminLogAdmin(ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'change_message', 'is_addition', 'is_change', 'is_deletion')
    list_filter = ['action_time', 'user', 'content_type']
    ordering = ('-action_time',)


@admin.register(MenuItem)
class MenuItemAdmin(ModelAdmin):
    list_display = ('id', 'name', 'path', 'context')


@admin.register(Host)
class HostAdmin(ModelAdmin):
    list_display = ('id', 'name', 'address', 'remote', 'created', 'updated')

