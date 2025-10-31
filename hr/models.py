import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from tenancy.models import AdministrativeUnit


class StaffProfile(models.Model):
    TEACHING = 'teaching'
    NON_TEACHING = 'non_teaching'

    ROLE_CHOICES = (
        (TEACHING, 'Teaching Staff'),
        (NON_TEACHING, 'Non-Teaching Staff'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    staff_number = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES)
    position = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=64, default='full_time')
    hire_date = models.DateField(default=timezone.now)
    termination_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    workload_hours = models.PositiveIntegerField(default=0)
    jurisdictions = models.ManyToManyField(AdministrativeUnit, blank=True)

    class Meta:
        ordering = ('staff_number',)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} ({self.staff_number})"


class StaffTransfer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='transfers')
    from_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.SET_NULL, null=True, related_name='staff_transfer_from')
    to_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.SET_NULL, null=True, related_name='staff_transfer_to')
    requested_on = models.DateField(default=timezone.now)
    approved_on = models.DateField(null=True, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)


class StaffPerformanceReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='performance_reviews')
    period_start = models.DateField()
    period_end = models.DateField()
    overall_score = models.DecimalField(max_digits=5, decimal_places=2)
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    strengths = models.TextField(blank=True)
    areas_of_improvement = models.TextField(blank=True)
    development_plan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class StaffCertification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    issuing_authority = models.CharField(max_length=255, blank=True)
    issued_on = models.DateField()
    expires_on = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)


class StaffAttendance(models.Model):
    PRESENT = 'present'
    ABSENT = 'absent'
    LATE = 'late'

    STATUS_CHOICES = (
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (LATE, 'Late'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('staff', 'date')


class LeaveType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    max_days = models.PositiveIntegerField(default=30)

    def __str__(self) -> str:
        return self.name


class LeaveRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CANCELLED, 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=PENDING)
    submitted_on = models.DateField(default=timezone.now)
    approved_on = models.DateField(null=True, blank=True)
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True)

    def duration(self):
        return (self.end_date - self.start_date).days + 1


class SubstituteAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    leave_request = models.OneToOneField(LeaveRequest, on_delete=models.CASCADE, related_name='substitute_assignment')
    substitute = models.ForeignKey(StaffProfile, on_delete=models.SET_NULL, null=True, related_name='substitute_assignments')
    notes = models.TextField(blank=True)
