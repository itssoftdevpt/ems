from django.contrib import admin

from organizations.models import ModuleToggle, SchoolProfile, TenantSetting


class ModuleToggleInline(admin.TabularInline):
    model = ModuleToggle
    extra = 0


@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_type', 'management_type')
    inlines = (ModuleToggleInline,)


@admin.register(TenantSetting)
class TenantSettingAdmin(admin.ModelAdmin):
    list_display = ('school', 'primary_color', 'theme_mode')


@admin.register(ModuleToggle)
class ModuleToggleAdmin(admin.ModelAdmin):
    list_display = ('school', 'module_key', 'is_enabled')
    list_filter = ('module_key', 'is_enabled')
