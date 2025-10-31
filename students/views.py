from django.db.models import Q
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from accounts.permissions import IsParent, IsStudent, IsTeachingStaff
from students.models import StudentAttendance, StudentDocument, StudentProfile
from students.serializers import (
    StudentAttendanceSerializer,
    StudentDocumentSerializer,
    StudentPortalSummarySerializer,
    StudentProfileCreateSerializer,
    StudentProfileSerializer,
)


class StudentProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = StudentProfile.objects.select_related('user', 'current_classroom', 'current_level').prefetch_related(
        'guardian_relationships__guardian'
    )

    def get_serializer_class(self):
        if self.action in {'create', 'partial_update', 'update'}:
            return StudentProfileCreateSerializer
        if self.action == 'portal_summary':
            return StudentPortalSummarySerializer
        return StudentProfileSerializer

    def get_queryset(self):
        user: User = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.role == User.ADMINISTRATOR:
            return qs
        if user.role == User.TEACHING_STAFF:
            return qs.filter(Q(advisors=user) | Q(current_classroom__subject_allocations__teacher=user)).distinct()
        if user.role == User.NON_TEACHING_STAFF:
            return qs
        if user.role == User.PARENT:
            return qs.filter(guardians=user)
        if user.role == User.STUDENT:
            return qs.filter(user=user)
        return qs.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        response = StudentProfileSerializer(student)
        headers = self.get_success_headers(response.data)
        return Response(response.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'], permission_classes=(IsAuthenticated, IsStudent))
    def my_profile(self, request):
        profile = StudentProfile.objects.filter(user=request.user).first()
        if not profile:
            return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=(IsAuthenticated, IsParent))
    def my_children(self, request):
        profiles = self.get_queryset().filter(guardians=request.user)
        serializer = StudentPortalSummarySerializer(profiles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=(IsAuthenticated,))
    def portal_summary(self, request, pk=None):
        student = self.get_object()
        serializer = StudentPortalSummarySerializer(student)
        return Response(serializer.data)


class StudentAttendanceViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsTeachingStaff)
    serializer_class = StudentAttendanceSerializer
    queryset = StudentAttendance.objects.select_related('student', 'classroom')

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(
            Q(student__advisors=user)
            | Q(student__current_classroom__subject_allocations__teacher=user)
            | Q(recorded_by=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)


class StudentDocumentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentDocumentSerializer
    queryset = StudentDocument.objects.select_related('student')

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or user.role == User.ADMINISTRATOR:
            return qs
        if user.role == User.TEACHING_STAFF:
            return qs.filter(student__advisors=user)
        if user.role == User.NON_TEACHING_STAFF:
            return qs
        if user.role == User.PARENT:
            return qs.filter(student__guardians=user)
        if user.role == User.STUDENT:
            return qs.filter(student__user=user)
        return qs.none()
