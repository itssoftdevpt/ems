import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from tenancy.models import AdministrativeUnit


class User(AbstractUser):
    """Custom user with tenant-specific roles and jurisdiction."""

    PARENT = 'parent'
    STUDENT = 'student'
    TEACHING_STAFF = 'teaching_staff'
    NON_TEACHING_STAFF = 'non_teaching_staff'
    ADMINISTRATOR = 'administrator'

    ROLE_CHOICES = (
        (PARENT, 'Parent / Guardian'),
        (STUDENT, 'Student'),
        (TEACHING_STAFF, 'Teaching Staff'),
        (NON_TEACHING_STAFF, 'Non-Teaching Staff'),
        (ADMINISTRATOR, 'Administrator'),
    )

    global_id = models.UUIDField(default=uuid.uuid4, unique=True)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default=ADMINISTRATOR)
    phone_number = models.CharField(
        max_length=32,
        blank=True,
        validators=[RegexValidator(r"^[+0-9\- ]*$", "Enter a valid phone number")],
    )
    assigned_units = models.ManyToManyField(
        AdministrativeUnit,
        blank=True,
        help_text='Administrative units the user has access to. Used for non-teaching staff.',
    )
    is_tenant_admin = models.BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        indexes = [
            models.Index(fields=('role',)),
            models.Index(fields=('username',)),
        ]

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"

    @property
    def display_role(self) -> str:
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

    def has_unit_access(self, unit: AdministrativeUnit) -> bool:
        if self.role == self.ADMINISTRATOR or self.is_superuser:
            return True
        if not unit:
            return False
        if self.assigned_units.filter(pk=unit.pk).exists():
            return True
        parent = unit.parent
        while parent is not None:
            if self.assigned_units.filter(pk=parent.pk).exists():
                return True
            parent = parent.parent
        return False
