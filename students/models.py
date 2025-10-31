import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from academics.models import AcademicLevel, Classroom, Subject
from tenancy.models import StudentTransferRequest


class GuardianRelationship(models.Model):
    PARENT = 'parent'
    GUARDIAN = 'guardian'

    RELATIONSHIP_CHOICES = (
        (PARENT, 'Parent'),
        (GUARDIAN, 'Guardian'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='guardian_relationships')
    guardian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guardian_relationships')
    relationship = models.CharField(max_length=32, choices=RELATIONSHIP_CHOICES)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'guardian', 'relationship')

    def __str__(self) -> str:
        return f"{self.guardian} -> {self.student} ({self.relationship})"


class StudentProfile(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    GRADUATED = 'graduated'
    WITHDRAWN = 'withdrawn'

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (GRADUATED, 'Graduated'),
        (WITHDRAWN, 'Withdrawn'),
    )

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_student_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=ACTIVE)
    enrolment_date = models.DateField(default=timezone.now)
    current_level = models.ForeignKey(
        AcademicLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
    )
    current_classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
    )
    guardians = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through=GuardianRelationship,
        related_name='wards',
    )
    advisors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='advised_students',
    )

    class Meta:
        ordering = ('admission_number',)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} ({self.admission_number})"


class EnrollmentRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.CharField(max_length=32)
    term = models.CharField(max_length=32)
    level = models.ForeignKey(AcademicLevel, on_delete=models.SET_NULL, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    is_promoted = models.BooleanField(default=False)
    registered_on = models.DateField(default=timezone.now)

    class Meta:
        ordering = ('-registered_on',)
        unique_together = ('student', 'academic_year', 'term')

    def __str__(self) -> str:
        return f"{self.student} - {self.academic_year} {self.term}"


class StudentAttendance(models.Model):
    PRESENT = 'present'
    ABSENT = 'absent'
    LATE = 'late'

    STATUS_CHOICES = (
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (LATE, 'Late'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_records')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ('-date',)

    def __str__(self) -> str:
        return f"{self.student} - {self.date}: {self.status}"


class StudentSubjectRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='subject_records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=32)
    term = models.CharField(max_length=32)
    continuous_assessment = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade = models.CharField(max_length=5, blank=True)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('student', 'subject', 'academic_year', 'term')


class StudentTransferHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='transfer_history')
    transfer_request = models.ForeignKey(StudentTransferRequest, on_delete=models.SET_NULL, null=True, blank=True)
    from_school_schema = models.CharField(max_length=63)
    to_school_schema = models.CharField(max_length=63)
    completed_on = models.DateTimeField(default=timezone.now)
    remarks = models.TextField(blank=True)


class StudentDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    document_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return self.title
