import uuid
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django_tenants.models import DomainMixin, TenantMixin


class ManagementGroup(models.Model):
    """Represents the ownership or management entity for schools."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    logo_url = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(
        max_length=32,
        blank=True,
        validators=[RegexValidator(r"^[+0-9\- ]*$", "Enter a valid phone number")],
    )
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class AdministrativeUnit(models.Model):
    """Hierarchical administrative unit (national/region/district/circuit/school)."""

    NATIONAL = 'national'
    REGION = 'region'
    DISTRICT = 'district'
    CIRCUIT = 'circuit'
    SCHOOL = 'school'

    LEVEL_CHOICES = (
        (NATIONAL, 'National'),
        (REGION, 'Region'),
        (DISTRICT, 'District'),
        (CIRCUIT, 'Circuit'),
        (SCHOOL, 'School'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=32, choices=LEVEL_CHOICES)
    code = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )
    management_group = models.ForeignKey(
        ManagementGroup,
        on_delete=models.PROTECT,
        related_name='administrative_units',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('level', 'name')
        unique_together = (
            ('name', 'level', 'parent'),
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.level})"


class Client(TenantMixin):
    """Tenant schema for an individual school."""

    MANAGEMENT_TYPES = (
        ('government', 'Government'),
        ('ngo', 'NGO'),
        ('religious', 'Religious Organization or Mission'),
        ('llc', 'Limited Liability Company'),
        ('sole_proprietorship', 'Sole Proprietorship'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schema_name = models.CharField(max_length=63, unique=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100, blank=True)
    management_group = models.ForeignKey(
        ManagementGroup,
        on_delete=models.PROTECT,
        related_name='tenants',
    )
    administrative_unit = models.ForeignKey(
        AdministrativeUnit,
        on_delete=models.PROTECT,
        related_name='tenants',
    )
    management_type = models.CharField(max_length=64, choices=MANAGEMENT_TYPES)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(
        max_length=32,
        blank=True,
        validators=[RegexValidator(r"^[+0-9\- ]*$", "Enter a valid phone number")],
    )
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    auto_create_schema = True

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Domain(DomainMixin):
    """Domain mapping for tenants."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self) -> str:
        return self.domain


class StudentTransferRequest(models.Model):
    """Tracks student transfers across tenants."""

    PENDING = 'pending'
    APPROVED = 'approved'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (PENDING, 'Pending Approval'),
        (APPROVED, 'Approved'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_global_id = models.UUIDField()
    from_tenant = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='transfer_requests_out',
    )
    to_tenant = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='transfer_requests_in',
    )
    confirmation_code = models.CharField(max_length=12)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='initiated_transfers',
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=PENDING)
    approved_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def mark_approved(self):
        self.status = self.APPROVED
        self.approved_at = timezone.now()
        self.save(update_fields=['status', 'approved_at', 'updated_at'])

    def mark_completed(self):
        self.status = self.COMPLETED
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at', 'updated_at'])

    def cancel(self):
        self.status = self.CANCELLED
        self.save(update_fields=['status', 'updated_at'])

    def __str__(self) -> str:
        return f"Transfer {self.student_global_id} -> {self.to_tenant} ({self.status})"
