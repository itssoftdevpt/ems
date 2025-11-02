from rest_framework.routers import DefaultRouter
from django.urls import path, include

from tenancy.views import (
    AdministrativeUnitViewSet,
    AggregatedMetricsView,
    ClientViewSet,
    ManagementGroupViewSet,
    StudentTransferInitiateView,
    StudentTransferRequestViewSet,
)

router = DefaultRouter()
router.register('management-groups', ManagementGroupViewSet, basename='management-group')
router.register('administrative-units', AdministrativeUnitViewSet, basename='administrative-unit')
router.register('clients', ClientViewSet, basename='client')
router.register('transfers', StudentTransferRequestViewSet, basename='transfer-request')

urlpatterns = [
    path('', include(router.urls)),
    path('transfers/initiate/', StudentTransferInitiateView.as_view(), name='transfer-initiate'),
    path('metrics/', AggregatedMetricsView.as_view(), name='aggregated-metrics'),
]
