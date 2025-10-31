from django.contrib import admin

from fees.models import (
    BankAccount,
    DiscountPolicy,
    FeeComponent,
    FeeSchedule,
    FeeStructure,
    Invoice,
    InvoiceLineItem,
    Payment,
    PaymentAllocation,
    Scholarship,
)


class FeeComponentInline(admin.TabularInline):
    model = FeeComponent
    extra = 0


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('name', 'applies_to_management_group', 'is_independent')
    inlines = (FeeComponentInline,)


@admin.register(FeeSchedule)
class FeeScheduleAdmin(admin.ModelAdmin):
    list_display = ('structure', 'component', 'academic_year', 'term', 'amount', 'level')
    list_filter = ('academic_year', 'term')


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'bank_name', 'account_number', 'level', 'is_active')
    list_filter = ('level', 'is_active')


@admin.register(DiscountPolicy)
class DiscountPolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'applies_to_level', 'applies_to_component')


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('student', 'name', 'amount', 'start_year', 'end_year')


class InvoiceLineItemInline(admin.TabularInline):
    model = InvoiceLineItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'term', 'status', 'total_amount')
    list_filter = ('academic_year', 'term', 'status')
    inlines = (InvoiceLineItemInline,)


class PaymentAllocationInline(admin.TabularInline):
    model = PaymentAllocation
    extra = 0


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'paid_on', 'reference', 'received_by')
    list_filter = ('paid_on',)
    inlines = (PaymentAllocationInline,)
