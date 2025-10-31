from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsNonTeachingStaff
from calendars.models import AcademicCalendar, AcademicTerm, EventBooking, Holiday
from calendars.serializers import (
    AcademicCalendarSerializer,
    AcademicTermSerializer,
    EventBookingSerializer,
    HolidaySerializer,
)


class AcademicCalendarViewSet(viewsets.ModelViewSet):
    queryset = AcademicCalendar.objects.prefetch_related('terms', 'holidays')
    serializer_class = AcademicCalendarSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]


class AcademicTermViewSet(viewsets.ModelViewSet):
    queryset = AcademicTerm.objects.select_related('calendar')
    serializer_class = AcademicTermSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]


class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.select_related('calendar')
    serializer_class = HolidaySerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]


class EventBookingViewSet(viewsets.ModelViewSet):
    queryset = EventBooking.objects.select_related('calendar', 'created_by')
    serializer_class = EventBookingSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
