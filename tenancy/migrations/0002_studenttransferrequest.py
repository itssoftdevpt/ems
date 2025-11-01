from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tenancy', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentTransferRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('student_global_id', models.UUIDField()),
                ('confirmation_code', models.CharField(max_length=12)),
                ('status', models.CharField(choices=[('pending', 'Pending Approval'), ('approved', 'Approved'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=32)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('from_tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_requests_out', to='tenancy.client')),
                ('requested_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='initiated_transfers', to=settings.AUTH_USER_MODEL)),
                ('to_tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_requests_in', to='tenancy.client')),
            ],
            options={'ordering': ('-created_at',)},
        ),
    ]
