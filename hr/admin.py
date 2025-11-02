from django.contrib import admin

from hr.models import (
    LeaveRequest,
    LeaveType,
    StaffAttendance,
    StaffCertification,
    StaffPerformanceReview,
    StaffProfile,
    StaffTransfer,
    SubstituteAssignment,
)


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('staff_number', 'user', 'role', 'position', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('staff_number', 'user__first_name', 'user__last_name')


@admin.register(StaffTransfer)
class StaffTransferAdmin(admin.ModelAdmin):
    list_display = ('staff', 'from_unit', 'to_unit', 'requested_on', 'effective_date')
    list_filter = ('requested_on', 'effective_date')


@admin.register(StaffPerformanceReview)
class StaffPerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('staff', 'period_start', 'period_end', 'overall_score', 'evaluator')


@admin.register(StaffCertification)
class StaffCertificationAdmin(admin.ModelAdmin):
    list_display = ('staff', 'name', 'issuing_authority', 'issued_on', 'expires_on')


@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'status', 'recorded_by')
    list_filter = ('status',)


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_days')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('staff', 'leave_type', 'start_date', 'end_date', 'status', 'approver')
    list_filter = ('status', 'start_date')


@admin.register(SubstituteAssignment)
class SubstituteAssignmentAdmin(admin.ModelAdmin):
    list_display = ('leave_request', 'substitute')
