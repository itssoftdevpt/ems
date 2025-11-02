from rest_framework import serializers

from organizations.models import ModuleToggle, SchoolProfile, TenantSetting


class ModuleToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleToggle
        fields = ('id', 'module_key', 'is_enabled', 'configuration')
        read_only_fields = ('id',)


class TenantSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSetting
        fields = (
            'logo_url',
            'primary_color',
            'secondary_color',
            'theme_mode',
            'additional_metadata',
        )


class SchoolProfileSerializer(serializers.ModelSerializer):
    settings = TenantSettingSerializer(read_only=True)
    module_toggles = ModuleToggleSerializer(many=True, read_only=True)

    class Meta:
        model = SchoolProfile
        fields = (
            'id',
            'external_school_id',
            'name',
            'motto',
            'vision',
            'mission',
            'school_type',
            'management_type',
            'established_on',
            'contact_email',
            'contact_phone',
            'address',
            'location',
            'created_at',
            'updated_at',
            'settings',
            'module_toggles',
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'settings', 'module_toggles')


class SchoolProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolProfile
        fields = (
            'external_school_id',
            'name',
            'motto',
            'vision',
            'mission',
            'school_type',
            'management_type',
            'established_on',
            'contact_email',
            'contact_phone',
            'address',
            'location',
        )
        extra_kwargs = {'external_school_id': {'required': False}}

class SchoolProfileUpdateSerializer(serializers.ModelSerializer):
    settings = TenantSettingSerializer()
    module_toggles = ModuleToggleSerializer(many=True)

    class Meta:
        model = SchoolProfile
        fields = (
            'name',
            'motto',
            'vision',
            'mission',
            'contact_email',
            'contact_phone',
            'address',
            'location',
            'settings',
            'module_toggles',
        )

    def update(self, instance, validated_data):
        settings_data = validated_data.pop('settings', None)
        module_data = validated_data.pop('module_toggles', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if settings_data:
            TenantSetting.objects.update_or_create(school=instance, defaults=settings_data)

        if module_data:
            existing = {toggle.module_key: toggle for toggle in instance.module_toggles.all()}
            for toggle in module_data:
                module_key = toggle['module_key']
                defaults = {
                    'is_enabled': toggle.get('is_enabled', True),
                    'configuration': toggle.get('configuration', {}),
                }
                ModuleToggle.objects.update_or_create(school=instance, module_key=module_key, defaults=defaults)
            for module_key, toggle in existing.items():
                if module_key not in {m['module_key'] for m in module_data}:
                    toggle.delete()
        return instance
