from django.contrib import admin

from tenancy.models import AdministrativeUnit, Client, Domain, ManagementGroup, StudentTransferRequest


@admin.register(ManagementGroup)
class ManagementGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'contact_phone')
    search_fields = ('name',)


@admin.register(AdministrativeUnit)
class AdministrativeUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'code', 'parent')
    list_filter = ('level',)
    search_fields = ('name', 'code')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'management_group', 'administrative_unit', 'management_type')
    list_filter = ('management_type', 'management_group')
    search_fields = ('name', 'schema_name')


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    search_fields = ('domain',)


@admin.register(StudentTransferRequest)
class StudentTransferRequestAdmin(admin.ModelAdmin):
    list_display = ('student_global_id', 'from_tenant', 'to_tenant', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('student_global_id',)
