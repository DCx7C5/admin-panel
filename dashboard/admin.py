from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session


class SessionAdmin(ModelAdmin):
    list_display = ('session_key', '_session_data', 'expire_date')


class AdminLogAdmin(ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'change_message', 'is_addition', 'is_change', 'is_deletion')
    list_filter = ['action_time', 'user', 'content_type']
    ordering = ('-action_time',)


admin.site.register(Session, SessionAdmin)
admin.site.register(LogEntry, AdminLogAdmin)
