from django.utils.crypto import get_random_string
from rest_framework import serializers

from .models import (
    AdministrativeUnit,
    Client,
    Domain,
    ManagementGroup,
    StudentTransferRequest,
)


class ManagementGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementGroup
        fields = (
            'id',
            'name',
            'logo_url',
            'contact_email',
            'contact_phone',
            'address',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class AdministrativeUnitSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AdministrativeUnit
        fields = (
            'id',
            'name',
            'level',
            'code',
            'parent',
            'management_group',
            'children',
        )
        read_only_fields = ('id', 'children')

    def get_children(self, obj):
        return AdministrativeUnitSerializer(obj.children.all(), many=True).data


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('id', 'domain', 'tenant', 'is_primary')
        read_only_fields = ('id',)


class ClientSerializer(serializers.ModelSerializer):
    domains = DomainSerializer(source='domain_set', many=True, read_only=True)

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'short_name',
            'schema_name',
            'management_group',
            'administrative_unit',
            'management_type',
            'contact_email',
            'contact_phone',
            'address',
            'domains',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_schema_name(self, value):
        return value.lower().replace('-', '_')


class ClientProvisionSerializer(ClientSerializer):
    domain = serializers.CharField(write_only=True)

    class Meta(ClientSerializer.Meta):
        fields = ClientSerializer.Meta.fields + ('domain',)

    def create(self, validated_data):
        domain_name = validated_data.pop('domain')
        tenant = super().create(validated_data)
        Domain.objects.create(
            domain=domain_name,
            tenant=tenant,
            is_primary=True,
        )
        return tenant


class StudentTransferRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTransferRequest
        fields = (
            'id',
            'student_global_id',
            'from_tenant',
            'to_tenant',
            'confirmation_code',
            'requested_by',
            'status',
            'approved_at',
            'completed_at',
            'metadata',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'status',
            'approved_at',
            'completed_at',
            'requested_by',
            'created_at',
            'updated_at',
        )

    def create(self, validated_data):
        if 'confirmation_code' not in validated_data:
            validated_data['confirmation_code'] = get_random_string(length=8).upper()
        return super().create(validated_data)
