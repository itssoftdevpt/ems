from django.contrib import admin

from students.models import (
    EnrollmentRecord,
    GuardianRelationship,
    StudentAttendance,
    StudentDocument,
    StudentProfile,
    StudentSubjectRecord,
    StudentTransferHistory,
)


class GuardianRelationshipInline(admin.TabularInline):
    model = GuardianRelationship
    extra = 0


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'user', 'status', 'current_classroom')
    list_filter = ('status',)
    search_fields = ('admission_number', 'user__first_name', 'user__last_name')
    inlines = (GuardianRelationshipInline,)


@admin.register(EnrollmentRecord)
class EnrollmentRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'term', 'level', 'classroom', 'is_promoted')
    list_filter = ('academic_year', 'term', 'is_promoted')


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'recorded_by')
    list_filter = ('status', 'date')


@admin.register(StudentSubjectRecord)
class StudentSubjectRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'academic_year', 'term', 'grade')
    list_filter = ('academic_year', 'term', 'grade')


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'uploaded_at')


@admin.register(StudentTransferHistory)
class StudentTransferHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'from_school_schema', 'to_school_schema', 'completed_on')
    list_filter = ('completed_on',)
