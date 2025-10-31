from django.contrib import admin

from communications.models import (
    Announcement,
    CalendarEvent,
    EventNotification,
    Message,
    MessageThread,
    NotificationPreference,
)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'target_level', 'created_at')
    list_filter = ('target_level', 'created_at')


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(MessageThread)
class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_by', 'created_at')
    inlines = (MessageInline,)


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_enabled', 'sms_enabled', 'push_enabled', 'whatsapp_enabled')


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_at', 'end_at', 'scope', 'scope_unit')
    list_filter = ('scope', 'start_at')


@admin.register(EventNotification)
class EventNotificationAdmin(admin.ModelAdmin):
    list_display = ('event', 'recipient', 'sent_at', 'channel', 'status')
    list_filter = ('channel', 'status')
