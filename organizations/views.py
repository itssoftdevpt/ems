from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from organizations.models import ModuleToggle, SchoolProfile, TenantSetting
from organizations.serializers import (
    ModuleToggleSerializer,
    SchoolProfileCreateSerializer,
    SchoolProfileSerializer,
    SchoolProfileUpdateSerializer,
    TenantSettingSerializer,
)


def get_school_profile() -> SchoolProfile:
    return SchoolProfile.objects.first()


class SchoolProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        school = get_school_profile()
        if not school:
            return Response({'detail': 'School profile not configured yet.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SchoolProfileSerializer(school)
        return Response(serializer.data)

    def post(self, request):
        if get_school_profile() is not None:
            return Response({'detail': 'Profile already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SchoolProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school = SchoolProfile.objects.create(**serializer.validated_data)
        TenantSetting.objects.get_or_create(school=school)
        response = SchoolProfileSerializer(school)
        return Response(response.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        school = get_school_profile()
        if not school:
            return Response({'detail': 'School profile not configured yet.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SchoolProfileUpdateSerializer(school, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        refreshed = SchoolProfileSerializer(school)
        return Response(refreshed.data)


class TenantBrandingView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        school = get_school_profile()
        if not school:
            return Response({'detail': 'School profile not configured yet.'}, status=status.HTTP_404_NOT_FOUND)
        settings = school.settings if hasattr(school, 'settings') else None
        if not settings:
            settings = TenantSetting.objects.create(school=school)
        serializer = TenantSettingSerializer(settings)
        return Response({'school_name': school.name, 'settings': serializer.data})


class ModuleToggleView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        school = get_school_profile()
        if not school:
            return Response({'detail': 'School profile not configured yet.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ModuleToggleSerializer(school.module_toggles.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        school = get_school_profile()
        if not school:
            return Response({'detail': 'School profile not configured yet.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ModuleToggleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ModuleToggle.objects.update_or_create(
            school=school,
            module_key=serializer.validated_data['module_key'],
            defaults={
                'is_enabled': serializer.validated_data.get('is_enabled', True),
                'configuration': serializer.validated_data.get('configuration', {}),
            },
        )
        return Response({'detail': 'Module toggle updated'}, status=status.HTTP_200_OK)
