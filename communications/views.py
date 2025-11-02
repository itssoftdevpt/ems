from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from accounts.permissions import IsNonTeachingStaff
from communications.models import (
    Announcement,
    CalendarEvent,
    EventNotification,
    Message,
    MessageThread,
    NotificationPreference,
)
from communications.serializers import (
    AnnouncementSerializer,
    CalendarEventSerializer,
    EventNotificationSerializer,
    MessageSerializer,
    MessageThreadCreateSerializer,
    MessageThreadSerializer,
    NotificationPreferenceSerializer,
)


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.select_related('created_by', 'target_unit')
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or user.role in {User.ADMINISTRATOR, User.NON_TEACHING_STAFF}:
            return qs
        if user.role == User.TEACHING_STAFF:
            return qs.filter(audience_roles__contains=[User.TEACHING_STAFF])
        if user.role == User.PARENT:
            return qs.filter(audience_roles__contains=[User.PARENT])
        if user.role == User.STUDENT:
            return qs.filter(audience_roles__contains=[User.STUDENT])
        return qs.none()


class MessageThreadViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = MessageThread.objects.prefetch_related('participants', 'messages__sender')
    serializer_class = MessageThreadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(participants=self.request.user)

    @action(detail=False, methods=['post'])
    def create_thread(self, request):
        serializer = MessageThreadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        thread = MessageThread.objects.create(subject=serializer.validated_data['subject'], created_by=request.user)
        participants = serializer.validated_data['participants'] + [request.user]
        thread.participants.set(participants)
        return Response(MessageThreadSerializer(thread, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        thread = self.get_object()
        if request.user not in thread.participants.all():
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        body = request.data.get('body', '').strip()
        if not body:
            return Response({'detail': 'Message body required'}, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.create(thread=thread, sender=request.user, body=body)
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    queryset = NotificationPreference.objects.select_related('user')
    serializer_class = NotificationPreferenceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.select_related('created_by', 'scope_unit')
    serializer_class = CalendarEventSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EventNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EventNotification.objects.select_related('event', 'recipient')
    serializer_class = EventNotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user)
