from django.urls import path
from rest_framework.routers import DefaultRouter

from reporting.views import ReportSnapshotViewSet, RealtimeMetricsView

router = DefaultRouter()
router.register('snapshots', ReportSnapshotViewSet, basename='report-snapshot')

urlpatterns = router.urls + [
    path('realtime/', RealtimeMetricsView.as_view(), name='realtime-metrics'),
]
