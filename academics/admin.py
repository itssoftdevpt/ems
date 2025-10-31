from django.contrib import admin

from academics.models import (
    AcademicLevel,
    Classroom,
    GradingScheme,
    LessonPlan,
    Programme,
    Section,
    Subject,
    SubjectAllocation,
    SyllabusProgress,
)


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('programme', 'name', 'order', 'recommended_class_size')
    list_filter = ('programme',)


@admin.register(AcademicLevel)
class AcademicLevelAdmin(admin.ModelAdmin):
    list_display = ('section', 'name', 'order')
    list_filter = ('section',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'level', 'workload_hours')
    search_fields = ('name', 'code')


@admin.register(GradingScheme)
class GradingSchemeAdmin(admin.ModelAdmin):
    list_display = ('section', 'grade', 'min_score', 'max_score')
    list_filter = ('section',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('level', 'name', 'stream', 'capacity', 'class_teacher')
    list_filter = ('level',)


@admin.register(SubjectAllocation)
class SubjectAllocationAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'subject', 'teacher', 'weekly_periods')
    list_filter = ('classroom', 'teacher')


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('subject', 'week_number', 'title', 'created_by', 'updated_at')
    list_filter = ('subject',)


@admin.register(SyllabusProgress)
class SyllabusProgressAdmin(admin.ModelAdmin):
    list_display = ('lesson_plan', 'completion_percentage', 'updated_by', 'updated_at')
    list_filter = ('lesson_plan__subject',)
