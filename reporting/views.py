from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsNonTeachingStaff
from reporting.models import ReportSnapshot
from reporting.serializers import ReportSnapshotSerializer
from tenancy.models import AdministrativeUnit
from tenancy.services import aggregation


class ReportSnapshotViewSet(viewsets.ModelViewSet):
    queryset = ReportSnapshot.objects.select_related('administrative_unit', 'created_by')
    serializer_class = ReportSnapshotSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RealtimeMetricsView(APIView):
    permission_classes = (IsAuthenticated, IsNonTeachingStaff)

    def get(self, request):
        unit_id = request.query_params.get('unit_id')
        category = request.query_params.get('category', 'students')
        unit = None
        if unit_id:
            unit = AdministrativeUnit.objects.filter(pk=unit_id).first()
        if category == 'staff':
            data = aggregation.staff_counts(unit)
        else:
            data = aggregation.student_counts(unit)
        return Response({'category': category, 'metrics': data}, status=status.HTTP_200_OK)
