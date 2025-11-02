from rest_framework import serializers

from reporting.models import ReportSnapshot


class ReportSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSnapshot
        fields = ('id', 'name', 'description', 'created_at', 'created_by', 'administrative_unit', 'payload')
        read_only_fields = ('id', 'created_at', 'created_by')
