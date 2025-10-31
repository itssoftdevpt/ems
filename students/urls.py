from rest_framework.routers import DefaultRouter

from students.views import StudentAttendanceViewSet, StudentDocumentViewSet, StudentProfileViewSet

router = DefaultRouter()
router.register('profiles', StudentProfileViewSet, basename='student-profile')
router.register('attendance', StudentAttendanceViewSet, basename='student-attendance')
router.register('documents', StudentDocumentViewSet, basename='student-document')

urlpatterns = router.urls
