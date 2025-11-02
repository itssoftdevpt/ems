from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.permissions import IsNonTeachingStaff, IsTeachingStaff
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
from hr.serializers import (
    LeaveRequestSerializer,
    LeaveTypeSerializer,
    StaffAttendanceSerializer,
    StaffCertificationSerializer,
    StaffPerformanceReviewSerializer,
    StaffProfileCreateSerializer,
    StaffProfileSerializer,
    StaffTransferSerializer,
    SubstituteAssignmentSerializer,
)


class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.select_related('user').prefetch_related('jurisdictions')

    def get_serializer_class(self):
        if self.action in {'create', 'update', 'partial_update'}:
            return StaffProfileCreateSerializer
        return StaffProfileSerializer

    def get_permissions(self):
        if self.action in {'list', 'retrieve'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]

    def get_queryset(self):
        user: User = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.role == User.ADMINISTRATOR:
            return qs
        if user.role == User.NON_TEACHING_STAFF:
            return qs.filter(jurisdictions__in=user.assigned_units.all()).distinct()
        if user.role == User.TEACHING_STAFF:
            return qs.filter(user=user)
        return qs.none()


class StaffTransferViewSet(viewsets.ModelViewSet):
    queryset = StaffTransfer.objects.select_related('staff', 'from_unit', 'to_unit')
    serializer_class = StaffTransferSerializer

    def get_permissions(self):
        if self.action in {'list', 'retrieve'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]


class StaffPerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = StaffPerformanceReview.objects.select_related('staff', 'evaluator')
    serializer_class = StaffPerformanceReviewSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsTeachingStaff()]


class StaffCertificationViewSet(viewsets.ModelViewSet):
    queryset = StaffCertification.objects.select_related('staff')
    serializer_class = StaffCertificationSerializer
    permission_classes = (IsAuthenticated,)


class StaffAttendanceViewSet(viewsets.ModelViewSet):
    queryset = StaffAttendance.objects.select_related('staff', 'recorded_by')
    serializer_class = StaffAttendanceSerializer
    permission_classes = (IsAuthenticated, IsNonTeachingStaff)

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)


class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.select_related('staff', 'leave_type', 'approver')
    serializer_class = LeaveRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or user.role == User.ADMINISTRATOR:
            return qs
        if user.role == User.NON_TEACHING_STAFF:
            return qs.filter(staff__jurisdictions__in=user.assigned_units.all()).distinct()
        if user.role == User.TEACHING_STAFF:
            return qs.filter(staff__user=user)
        return qs.none()

    def perform_update(self, serializer):
        if serializer.validated_data.get('status') in {LeaveRequest.APPROVED, LeaveRequest.REJECTED}:
            serializer.save(approver=self.request.user)
        else:
            serializer.save()


class SubstituteAssignmentViewSet(viewsets.ModelViewSet):
    queryset = SubstituteAssignment.objects.select_related('leave_request', 'substitute')
    serializer_class = SubstituteAssignmentSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]
