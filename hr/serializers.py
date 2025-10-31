from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.serializers import UserSerializer
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

User = get_user_model()


class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StaffProfile
        fields = (
            'id',
            'user',
            'staff_number',
            'role',
            'position',
            'employment_type',
            'hire_date',
            'termination_date',
            'is_active',
            'workload_hours',
            'jurisdictions',
        )
        read_only_fields = ('id',)


class StaffProfileCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StaffProfile
        fields = (
            'user',
            'staff_number',
            'role',
            'position',
            'employment_type',
            'hire_date',
            'jurisdictions',
        )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        role = user_data.get('role', User.NON_TEACHING_STAFF)
        defaults = {
            'role': role,
            'first_name': user_data.get('first_name', ''),
            'last_name': user_data.get('last_name', ''),
            'email': user_data.get('email', ''),
        }
        password = user_data.get('password')
        user, created = User.objects.get_or_create(username=user_data['username'], defaults=defaults)
        if created and password:
            user.set_password(password)
            user.save(update_fields=['password'])
        staff = StaffProfile.objects.create(user=user, **validated_data)
        staff.jurisdictions.set(validated_data.get('jurisdictions', []))
        return staff


class StaffTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTransfer
        fields = (
            'id',
            'staff',
            'from_unit',
            'to_unit',
            'requested_on',
            'approved_on',
            'effective_date',
            'notes',
        )
        read_only_fields = ('id',)


class StaffPerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPerformanceReview
        fields = (
            'id',
            'staff',
            'period_start',
            'period_end',
            'overall_score',
            'evaluator',
            'strengths',
            'areas_of_improvement',
            'development_plan',
            'created_at',
        )
        read_only_fields = ('id', 'created_at')


class StaffCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffCertification
        fields = ('id', 'staff', 'name', 'issuing_authority', 'issued_on', 'expires_on', 'credential_url')
        read_only_fields = ('id',)


class StaffAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAttendance
        fields = ('id', 'staff', 'date', 'status', 'remarks')
        read_only_fields = ('id',)


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ('id', 'name', 'description', 'max_days')
        read_only_fields = ('id',)


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = (
            'id',
            'staff',
            'leave_type',
            'start_date',
            'end_date',
            'status',
            'submitted_on',
            'approved_on',
            'approver',
            'reason',
        )
        read_only_fields = ('id', 'submitted_on', 'approved_on', 'approver')


class SubstituteAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstituteAssignment
        fields = ('id', 'leave_request', 'substitute', 'notes')
        read_only_fields = ('id',)
