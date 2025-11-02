from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.permissions import IsTeachingStaff
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
from academics.serializers import (
    AcademicLevelSerializer,
    ClassroomSerializer,
    GradingSchemeSerializer,
    LessonPlanSerializer,
    ProgrammeSerializer,
    SectionSerializer,
    SubjectAllocationSerializer,
    SubjectSerializer,
    SyllabusProgressSerializer,
)


class StaffWritePermissionMixin:
    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [IsAuthenticated()]
        user: User = self.request.user
        if user.is_superuser or user.role in {User.ADMINISTRATOR, User.TEACHING_STAFF}:
            return [IsAuthenticated()]
        return [IsTeachingStaff()]


class ProgrammeViewSet(StaffWritePermissionMixin, viewsets.ModelViewSet):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeSerializer


class SectionViewSet(StaffWritePermissionMixin, viewsets.ModelViewSet):
    queryset = Section.objects.select_related('programme')
    serializer_class = SectionSerializer


class AcademicLevelViewSet(StaffWritePermissionMixin, viewsets.ModelViewSet):
    queryset = AcademicLevel.objects.select_related('section', 'section__programme')
    serializer_class = AcademicLevelSerializer


class SubjectViewSet(StaffWritePermissionMixin, viewsets.ModelViewSet):
    queryset = Subject.objects.select_related('level', 'level__section')
    serializer_class = SubjectSerializer


class GradingSchemeViewSet(StaffWritePermissionMixin, viewsets.ModelViewSet):
    queryset = GradingScheme.objects.select_related('section')
    serializer_class = GradingSchemeSerializer


class ClassroomViewSet(StaffWritePermissionMixin, viewsets.ModelViewSet):
    queryset = Classroom.objects.select_related('level', 'level__section', 'class_teacher', 'coordinator')
    serializer_class = ClassroomSerializer


class SubjectAllocationViewSet(StaffWritePermissionMixin, viewsets.ModelViewSet):
    queryset = SubjectAllocation.objects.select_related('classroom', 'subject', 'teacher')
    serializer_class = SubjectAllocationSerializer


class LessonPlanViewSet(StaffWritePermissionMixin, viewsets.ModelViewSet):
    queryset = LessonPlan.objects.select_related('subject', 'created_by')
    serializer_class = LessonPlanSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SyllabusProgressViewSet(StaffWritePermissionMixin, viewsets.ModelViewSet):
    queryset = SyllabusProgress.objects.select_related('lesson_plan', 'updated_by')
    serializer_class = SyllabusProgressSerializer

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
