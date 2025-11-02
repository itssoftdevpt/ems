from rest_framework.routers import DefaultRouter

from hr.views import (
    LeaveRequestViewSet,
    LeaveTypeViewSet,
    StaffAttendanceViewSet,
    StaffCertificationViewSet,
    StaffPerformanceReviewViewSet,
    StaffProfileViewSet,
    StaffTransferViewSet,
    SubstituteAssignmentViewSet,
)

router = DefaultRouter()
router.register('profiles', StaffProfileViewSet, basename='staff-profile')
router.register('transfers', StaffTransferViewSet, basename='staff-transfer')
router.register('performance', StaffPerformanceReviewViewSet, basename='staff-performance')
router.register('certifications', StaffCertificationViewSet, basename='staff-certification')
router.register('attendance', StaffAttendanceViewSet, basename='staff-attendance')
router.register('leave-types', LeaveTypeViewSet, basename='leave-type')
router.register('leave-requests', LeaveRequestViewSet, basename='leave-request')
router.register('substitutes', SubstituteAssignmentViewSet, basename='substitute-assignment')

urlpatterns = router.urls
