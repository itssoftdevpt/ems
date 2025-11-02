from rest_framework import serializers

from calendars.models import AcademicCalendar, AcademicTerm, EventBooking, Holiday


class AcademicTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicTerm
        fields = ('id', 'name', 'start_date', 'end_date', 'registration_start', 'registration_end')
        read_only_fields = ('id',)


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ('id', 'name', 'date', 'scope')
        read_only_fields = ('id',)


class AcademicCalendarSerializer(serializers.ModelSerializer):
    terms = AcademicTermSerializer(many=True, read_only=True)
    holidays = HolidaySerializer(many=True, read_only=True)

    class Meta:
        model = AcademicCalendar
        fields = ('id', 'management_group', 'academic_year', 'description', 'is_active', 'terms', 'holidays')
        read_only_fields = ('id',)


class EventBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = ('id', 'calendar', 'title', 'description', 'start_at', 'end_at', 'location', 'created_by')
        read_only_fields = ('id', 'created_by')
