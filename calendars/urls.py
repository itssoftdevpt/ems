from rest_framework.routers import DefaultRouter

from calendars.views import AcademicCalendarViewSet, AcademicTermViewSet, EventBookingViewSet, HolidayViewSet

router = DefaultRouter()
router.register('calendars', AcademicCalendarViewSet, basename='academic-calendar')
router.register('terms', AcademicTermViewSet, basename='academic-term')
router.register('holidays', HolidayViewSet, basename='holiday')
router.register('events', EventBookingViewSet, basename='event-booking')

urlpatterns = router.urls
