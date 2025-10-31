import uuid

from django.db import models


class SchoolProfile(models.Model):
    """Tenant-scoped metadata about the school."""

    PUBLIC = 'public'
    PRIVATE = 'private'

    SCHOOL_TYPE_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_school_id = models.UUIDField(help_text='Globally unique school ID', unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    motto = models.CharField(max_length=255, blank=True)
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    school_type = models.CharField(max_length=32, choices=SCHOOL_TYPE_CHOICES)
    management_type = models.CharField(max_length=64)
    established_on = models.DateField(null=True, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=32, blank=True)
    address = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'School Profile'

    def __str__(self) -> str:
        return self.name


class TenantSetting(models.Model):
    """Customization preferences for the tenant."""

    school = models.OneToOneField(SchoolProfile, on_delete=models.CASCADE, related_name='settings')
    logo_url = models.URLField(blank=True)
    primary_color = models.CharField(max_length=16, default='#1D4ED8')
    secondary_color = models.CharField(max_length=16, default='#1E40AF')
    theme_mode = models.CharField(max_length=16, default='light')
    additional_metadata = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return f"Settings for {self.school.name}"


class ModuleToggle(models.Model):
    """Feature toggles for modules per tenant."""

    MODULE_CHOICES = (
        ('student_management', 'Student Management'),
        ('academic_management', 'Academic Management'),
        ('human_resources', 'Human Resources'),
        ('fees_management', 'Fees Management'),
        ('communications', 'Communications'),
        ('calendar', 'Calendar and Events'),
        ('security', 'Security and Safety'),
        ('reporting', 'Reporting and Analytics'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, related_name='module_toggles')
    module_key = models.CharField(max_length=64, choices=MODULE_CHOICES)
    is_enabled = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('school', 'module_key')
        verbose_name = 'Module Toggle'

    def __str__(self) -> str:
        return f"{self.module_key} ({'enabled' if self.is_enabled else 'disabled'})"
