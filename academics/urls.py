from rest_framework.routers import DefaultRouter

from academics.views import (
    AcademicLevelViewSet,
    ClassroomViewSet,
    GradingSchemeViewSet,
    LessonPlanViewSet,
    ProgrammeViewSet,
    SectionViewSet,
    SubjectAllocationViewSet,
    SubjectViewSet,
    SyllabusProgressViewSet,
)

router = DefaultRouter()
router.register('programmes', ProgrammeViewSet, basename='programme')
router.register('sections', SectionViewSet, basename='section')
router.register('levels', AcademicLevelViewSet, basename='level')
router.register('subjects', SubjectViewSet, basename='subject')
router.register('grading', GradingSchemeViewSet, basename='grading')
router.register('classrooms', ClassroomViewSet, basename='classroom')
router.register('subject-allocations', SubjectAllocationViewSet, basename='subject-allocation')
router.register('lesson-plans', LessonPlanViewSet, basename='lesson-plan')
router.register('syllabus-progress', SyllabusProgressViewSet, basename='syllabus-progress')

urlpatterns = router.urls
