from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SchoolProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_school_id', models.UUIDField(default=uuid.uuid4, help_text='Globally unique school ID', unique=True)),
                ('name', models.CharField(max_length=255)),
                ('motto', models.CharField(blank=True, max_length=255)),
                ('vision', models.TextField(blank=True)),
                ('mission', models.TextField(blank=True)),
                ('school_type', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], max_length=32)),
                ('management_type', models.CharField(max_length=64)),
                ('established_on', models.DateField(blank=True, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=32)),
                ('address', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'School Profile'},
        ),
        migrations.CreateModel(
            name='TenantSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_url', models.URLField(blank=True)),
                ('primary_color', models.CharField(default='#1D4ED8', max_length=16)),
                ('secondary_color', models.CharField(default='#1E40AF', max_length=16)),
                ('theme_mode', models.CharField(default='light', max_length=16)),
                ('additional_metadata', models.JSONField(blank=True, default=dict)),
                ('school', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='organizations.schoolprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ModuleToggle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('module_key', models.CharField(choices=[('student_management', 'Student Management'), ('academic_management', 'Academic Management'), ('human_resources', 'Human Resources'), ('fees_management', 'Fees Management'), ('communications', 'Communications'), ('calendar', 'Calendar and Events'), ('security', 'Security and Safety'), ('reporting', 'Reporting and Analytics')], max_length=64)),
                ('is_enabled', models.BooleanField(default=True)),
                ('configuration', models.JSONField(blank=True, default=dict)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='module_toggles', to='organizations.schoolprofile')),
            ],
            options={'verbose_name': 'Module Toggle', 'unique_together': {('school', 'module_key')}},
        ),
    ]
