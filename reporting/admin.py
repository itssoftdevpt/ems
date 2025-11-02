from django.contrib import admin

from reporting.models import ReportSnapshot


@admin.register(ReportSnapshot)
class ReportSnapshotAdmin(admin.ModelAdmin):
    list_display = ('name', 'administrative_unit', 'created_by', 'created_at')
    list_filter = ('administrative_unit',)
    search_fields = ('name',)
