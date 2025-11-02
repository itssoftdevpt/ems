from django.contrib import admin

from calendars.models import AcademicCalendar, AcademicTerm, EventBooking, Holiday


class AcademicTermInline(admin.TabularInline):
    model = AcademicTerm
    extra = 0


class HolidayInline(admin.TabularInline):
    model = Holiday
    extra = 0


@admin.register(AcademicCalendar)
class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('management_group', 'academic_year', 'is_active')
    list_filter = ('management_group', 'is_active')
    inlines = (AcademicTermInline, HolidayInline)


@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('title', 'calendar', 'start_at', 'end_at', 'location')
    list_filter = ('calendar',)
