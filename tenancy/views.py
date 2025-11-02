from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tenancy.models import (
    AdministrativeUnit,
    Client,
    ManagementGroup,
    StudentTransferRequest,
)
from tenancy.permissions import IsPlatformAdministrator
from tenancy.serializers import (
    AdministrativeUnitSerializer,
    ClientProvisionSerializer,
    ClientSerializer,
    ManagementGroupSerializer,
    StudentTransferRequestSerializer,
)
from tenancy.services import aggregation


class ManagementGroupViewSet(viewsets.ModelViewSet):
    queryset = ManagementGroup.objects.all()
    serializer_class = ManagementGroupSerializer
    permission_classes = (IsAuthenticated, IsPlatformAdministrator)


class AdministrativeUnitViewSet(viewsets.ModelViewSet):
    queryset = AdministrativeUnit.objects.select_related('parent', 'management_group')
    serializer_class = AdministrativeUnitSerializer
    permission_classes = (IsAuthenticated, IsPlatformAdministrator)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.select_related('management_group', 'administrative_unit')
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated, IsPlatformAdministrator)

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientProvisionSerializer
        return super().get_serializer_class()


class StudentTransferRequestViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = StudentTransferRequest.objects.select_related('from_tenant', 'to_tenant', 'requested_by')
    serializer_class = StudentTransferRequestSerializer
    permission_classes = (IsAuthenticated, IsPlatformAdministrator)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        transfer = self.get_object()
        transfer.mark_approved()
        serializer = self.get_serializer(transfer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        transfer = self.get_object()
        transfer.mark_completed()
        serializer = self.get_serializer(transfer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        transfer = self.get_object()
        transfer.cancel()
        serializer = self.get_serializer(transfer)
        return Response(serializer.data)


class StudentTransferInitiateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = StudentTransferRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transfer = serializer.save(requested_by=request.user)
        response = StudentTransferRequestSerializer(transfer)
        return Response(response.data, status=status.HTTP_201_CREATED)


class AggregatedMetricsView(APIView):
    permission_classes = (IsAuthenticated, IsPlatformAdministrator)

    def get(self, request):
        unit_id = request.query_params.get('unit_id')
        category = request.query_params.get('category', 'students')
        unit = None
        if unit_id:
            unit = get_object_or_404(AdministrativeUnit, pk=unit_id)

        if category == 'staff':
            data = aggregation.staff_counts(unit)
        else:
            data = aggregation.student_counts(unit)
        return Response({'category': category, 'unit': unit_id, 'metrics': data})
