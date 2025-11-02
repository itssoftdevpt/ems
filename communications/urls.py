from rest_framework.routers import DefaultRouter

from communications.views import (
    AnnouncementViewSet,
    CalendarEventViewSet,
    EventNotificationViewSet,
    MessageThreadViewSet,
    NotificationPreferenceViewSet,
)

router = DefaultRouter()
router.register('announcements', AnnouncementViewSet, basename='announcement')
router.register('threads', MessageThreadViewSet, basename='message-thread')
router.register('preferences', NotificationPreferenceViewSet, basename='notification-preference')
router.register('events', CalendarEventViewSet, basename='calendar-event')
router.register('event-notifications', EventNotificationViewSet, basename='event-notification')

urlpatterns = router.urls
