import uuid

from django.db import models

from tenancy.models import ManagementGroup


class AcademicCalendar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    management_group = models.ForeignKey(ManagementGroup, on_delete=models.CASCADE, related_name='academic_calendars')
    academic_year = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('management_group', 'academic_year')

    def __str__(self) -> str:
        return f"{self.management_group.name} - {self.academic_year}"


class AcademicTerm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    calendar = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, related_name='terms')
    name = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    registration_start = models.DateField(null=True, blank=True)
    registration_end = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('start_date',)

    def __str__(self) -> str:
        return f"{self.calendar.academic_year} - {self.name}"


class Holiday(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    calendar = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, related_name='holidays')
    name = models.CharField(max_length=255)
    date = models.DateField()
    scope = models.CharField(max_length=64, default='national')

    class Meta:
        ordering = ('date',)


class EventBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    calendar = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, related_name='event_bookings')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
