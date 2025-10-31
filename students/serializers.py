from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.serializers import UserSerializer
from academics.models import Classroom
from students.models import (
    EnrollmentRecord,
    GuardianRelationship,
    StudentAttendance,
    StudentDocument,
    StudentProfile,
    StudentSubjectRecord,
)

User = get_user_model()


class GuardianRelationshipSerializer(serializers.ModelSerializer):
    guardian = UserSerializer()

    class Meta:
        model = GuardianRelationship
        fields = ('id', 'guardian', 'relationship', 'is_primary')


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    guardians = GuardianRelationshipSerializer(source='guardian_relationships', many=True)

    class Meta:
        model = StudentProfile
        fields = (
            'id',
            'external_student_id',
            'user',
            'admission_number',
            'date_of_birth',
            'gender',
            'status',
            'enrolment_date',
            'current_level',
            'current_classroom',
            'guardians',
        )
        read_only_fields = ('id', 'external_student_id')


class StudentProfileCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    guardians = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        model = StudentProfile
        fields = (
            'user',
            'admission_number',
            'date_of_birth',
            'gender',
            'current_level',
            'current_classroom',
            'guardians',
        )

    def create(self, validated_data):
        guardian_data = validated_data.pop('guardians', [])
        user_data = validated_data.pop('user')
        user_defaults = {
            'first_name': user_data.get('first_name', ''),
            'last_name': user_data.get('last_name', ''),
            'email': user_data.get('email', ''),
        }
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data.get('password', User.objects.make_random_password()),
            role=User.STUDENT,
            **user_defaults,
        )
        student = StudentProfile.objects.create(user=user, **validated_data)

        for guardian in guardian_data:
            guardian_user, _ = User.objects.get_or_create(
                username=guardian['username'],
                defaults={
                    'role': User.PARENT,
                    'first_name': guardian.get('first_name', ''),
                    'last_name': guardian.get('last_name', ''),
                    'email': guardian.get('email', ''),
                },
            )
            GuardianRelationship.objects.update_or_create(
                student=student,
                guardian=guardian_user,
                defaults={
                    'relationship': guardian.get('relationship', GuardianRelationship.GUARDIAN),
                    'is_primary': guardian.get('is_primary', False),
                },
            )
        return student


class EnrollmentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentRecord
        fields = (
            'id',
            'academic_year',
            'term',
            'level',
            'classroom',
            'is_promoted',
            'registered_on',
        )
        read_only_fields = ('id', 'registered_on')


class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = (
            'id',
            'student',
            'classroom',
            'date',
            'status',
            'remarks',
        )
        read_only_fields = ('id',)

    def validate(self, attrs):
        classroom = attrs.get('classroom')
        student = attrs['student']
        if classroom and classroom != student.current_classroom:
            raise serializers.ValidationError('Student is not assigned to this classroom.')
        return attrs


class StudentSubjectRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubjectRecord
        fields = (
            'id',
            'student',
            'subject',
            'academic_year',
            'term',
            'continuous_assessment',
            'exam_score',
            'grade',
            'remarks',
        )
        read_only_fields = ('id',)


class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        fields = ('id', 'student', 'title', 'document_url', 'uploaded_at', 'metadata')
        read_only_fields = ('id', 'uploaded_at')


class StudentPortalSummarySerializer(serializers.ModelSerializer):
    classroom_name = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = (
            'id',
            'external_student_id',
            'admission_number',
            'status',
            'classroom_name',
        )

    def get_classroom_name(self, obj):
        classroom = obj.current_classroom
        if isinstance(classroom, Classroom):
            return str(classroom)
        return None
