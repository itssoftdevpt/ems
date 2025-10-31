from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            'SaaS Metadata',
            {'fields': ('role', 'global_id', 'phone_number', 'assigned_units', 'is_tenant_admin')},
        ),
    )
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'is_tenant_admin')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    filter_horizontal = ('assigned_units',)
