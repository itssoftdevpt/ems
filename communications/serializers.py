from rest_framework import serializers

from django.contrib.auth import get_user_model

from accounts.serializers import UserSerializer
from communications.models import (
    Announcement,
    CalendarEvent,
    EventNotification,
    Message,
    MessageThread,
    NotificationPreference,
)

User = get_user_model()


class AnnouncementSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = (
            'id',
            'title',
            'body',
            'created_by',
            'created_at',
            'target_level',
            'target_unit',
            'classroom_id',
            'audience_roles',
        )
        read_only_fields = ('id', 'created_at', 'created_by')


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'body', 'sent_at', 'read_by')
        read_only_fields = ('id', 'sender', 'sent_at', 'read_by')


class MessageThreadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = MessageThread
        fields = ('id', 'subject', 'created_by', 'participants', 'created_at', 'messages')
        read_only_fields = ('id', 'created_by', 'created_at', 'participants', 'messages')


class MessageThreadCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = MessageThread
        fields = ('subject', 'participants')


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ('id', 'user', 'sms_enabled', 'email_enabled', 'push_enabled', 'whatsapp_enabled', 'metadata')
        read_only_fields = ('id', 'user')


class CalendarEventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = CalendarEvent
        fields = (
            'id',
            'title',
            'description',
            'start_at',
            'end_at',
            'created_by',
            'scope',
            'scope_unit',
            'notify_participants',
        )
        read_only_fields = ('id', 'created_by')


class EventNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventNotification
        fields = ('id', 'event', 'recipient', 'sent_at', 'channel', 'status')
        read_only_fields = ('id', 'sent_at')
