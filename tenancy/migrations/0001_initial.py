from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ManagementGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('logo_url', models.URLField(blank=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=32)),
                ('address', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ('name',)},
        ),
        migrations.CreateModel(
            name='AdministrativeUnit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('level', models.CharField(choices=[('national', 'National'), ('region', 'Region'), ('district', 'District'), ('circuit', 'Circuit'), ('school', 'School')], max_length=32)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('management_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='administrative_units', to='tenancy.managementgroup')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='tenancy.administrativeunit')),
            ],
            options={'ordering': ('level', 'name'), 'unique_together': {('name', 'level', 'parent')}},
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('schema_name', models.CharField(max_length=63, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(blank=True, max_length=100)),
                ('management_type', models.CharField(choices=[('government', 'Government'), ('ngo', 'NGO'), ('religious', 'Religious Organization or Mission'), ('llc', 'Limited Liability Company'), ('sole_proprietorship', 'Sole Proprietorship')], max_length=64)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=32)),
                ('address', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('administrative_unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tenants', to='tenancy.administrativeunit')),
                ('management_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tenants', to='tenancy.managementgroup')),
            ],
            options={'ordering': ('name',)},
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('domain', models.CharField(max_length=253, unique=True)),
                ('is_primary', models.BooleanField(default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='tenancy.client')),
            ],
        ),
    ]
