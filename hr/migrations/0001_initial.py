from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenancy', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('max_days', models.PositiveIntegerField(default=30)),
            ],
        ),
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('staff_number', models.CharField(max_length=50, unique=True)),
                ('role', models.CharField(choices=[('teaching', 'Teaching Staff'), ('non_teaching', 'Non-Teaching Staff')], max_length=32)),
                ('position', models.CharField(max_length=255)),
                ('employment_type', models.CharField(default='full_time', max_length=64)),
                ('hire_date', models.DateField(default=django.utils.timezone.now)),
                ('termination_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('workload_hours', models.PositiveIntegerField(default=0)),
                ('jurisdictions', models.ManyToManyField(blank=True, to='tenancy.administrativeunit')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ('staff_number',)},
        ),
        migrations.CreateModel(
            name='StaffTransfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('requested_on', models.DateField(default=django.utils.timezone.now)),
                ('approved_on', models.DateField(blank=True, null=True)),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('from_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_transfer_from', to='tenancy.administrativeunit')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to='hr.staffprofile')),
                ('to_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_transfer_to', to='tenancy.administrativeunit')),
            ],
        ),
        migrations.CreateModel(
            name='StaffPerformanceReview',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('period_start', models.DateField()),
                ('period_end', models.DateField()),
                ('overall_score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('strengths', models.TextField(blank=True)),
                ('areas_of_improvement', models.TextField(blank=True)),
                ('development_plan', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('evaluator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_reviews', to='hr.staffprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StaffCertification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('issuing_authority', models.CharField(blank=True, max_length=255)),
                ('issued_on', models.DateField()),
                ('expires_on', models.DateField(blank=True, null=True)),
                ('credential_url', models.URLField(blank=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='hr.staffprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StaffAttendance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')], max_length=16)),
                ('remarks', models.TextField(blank=True)),
                ('recorded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='hr.staffprofile')),
            ],
            options={'unique_together': {('staff', 'date')}},
        ),
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], default='pending', max_length=32)),
                ('submitted_on', models.DateField(default=django.utils.timezone.now)),
                ('approved_on', models.DateField(blank=True, null=True)),
                ('reason', models.TextField(blank=True)),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('leave_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.leavetype')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', to='hr.staffprofile')),
            ],
        ),
        migrations.CreateModel(
            name='SubstituteAssignment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notes', models.TextField(blank=True)),
                ('leave_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='substitute_assignment', to='hr.leaverequest')),
                ('substitute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='substitute_assignments', to='hr.staffprofile')),
            ],
        ),
    ]
