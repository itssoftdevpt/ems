import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from academics.models import AcademicLevel
from tenancy.models import AdministrativeUnit, ManagementGroup


class BankAccount(models.Model):
    LEVEL_CHOICES = (
        ('national', 'National'),
        ('region', 'Region'),
        ('district', 'District'),
        ('circuit', 'Circuit'),
        ('school', 'School'),
        ('group', 'Management Group'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=64)
    bank_name = models.CharField(max_length=255)
    level = models.CharField(max_length=32, choices=LEVEL_CHOICES)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.SET_NULL, null=True, blank=True)
    management_group = models.ForeignKey(ManagementGroup, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.bank_name} - {self.account_number}"


class FeeStructure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    applies_to_management_group = models.ForeignKey(
        ManagementGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_independent = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class FeeComponent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='components')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        unique_together = ('structure', 'name')

    def __str__(self) -> str:
        return f"{self.structure.name} - {self.name}"


class FeeSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='schedules')
    academic_year = models.CharField(max_length=32)
    term = models.CharField(max_length=32)
    component = models.ForeignKey(FeeComponent, on_delete=models.CASCADE, related_name='schedules')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    level = models.ForeignKey(AcademicLevel, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('structure', 'academic_year', 'term', 'component', 'level')


class DiscountPolicy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    applies_to_level = models.ForeignKey(AcademicLevel, on_delete=models.SET_NULL, null=True, blank=True)
    applies_to_component = models.ForeignKey(FeeComponent, on_delete=models.SET_NULL, null=True, blank=True)


class Scholarship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='scholarships')
    name = models.CharField(max_length=255)
    discount_policy = models.ForeignKey(DiscountPolicy, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_year = models.CharField(max_length=32)
    end_year = models.CharField(max_length=32, blank=True)


class Invoice(models.Model):
    UNPAID = 'unpaid'
    PARTIAL = 'partial'
    PAID = 'paid'

    STATUS_CHOICES = (
        (UNPAID, 'Unpaid'),
        (PARTIAL, 'Partially Paid'),
        (PAID, 'Paid'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='invoices')
    academic_year = models.CharField(max_length=32)
    term = models.CharField(max_length=32)
    structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=UNPAID)
    issued_on = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class InvoiceLineItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='line_items')
    component = models.ForeignKey(FeeComponent, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField(default=timezone.now)
    reference = models.CharField(max_length=255, blank=True)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True)


class PaymentAllocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='allocations')
    line_item = models.ForeignKey(InvoiceLineItem, on_delete=models.CASCADE, related_name='allocations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
