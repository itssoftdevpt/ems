from rest_framework import serializers

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


class ProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programme
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'programme', 'name', 'order', 'recommended_class_size')
        read_only_fields = ('id',)


class AcademicLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicLevel
        fields = ('id', 'section', 'name', 'order')
        read_only_fields = ('id',)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'level', 'name', 'code', 'workload_hours')
        read_only_fields = ('id',)


class GradingSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingScheme
        fields = ('id', 'section', 'min_score', 'max_score', 'grade', 'remark')
        read_only_fields = ('id',)


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ('id', 'level', 'name', 'stream', 'capacity', 'coordinator', 'class_teacher')
        read_only_fields = ('id',)


class SubjectAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectAllocation
        fields = ('id', 'classroom', 'subject', 'teacher', 'weekly_periods')
        read_only_fields = ('id',)


class LessonPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        fields = ('id', 'subject', 'week_number', 'title', 'objectives', 'resources', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')


class SyllabusProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyllabusProgress
        fields = ('id', 'lesson_plan', 'completion_percentage', 'notes', 'updated_by', 'updated_at')
        read_only_fields = ('id', 'updated_at', 'updated_by')
