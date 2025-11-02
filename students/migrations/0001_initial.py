from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academics', '0001_initial'),
        ('tenancy', '0002_studenttransferrequest'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_student_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('admission_number', models.CharField(max_length=50, unique=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=16)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('graduated', 'Graduated'), ('withdrawn', 'Withdrawn')], default='active', max_length=32)),
                ('enrolment_date', models.DateField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
                ('advisors', models.ManyToManyField(blank=True, related_name='advised_students', to=settings.AUTH_USER_MODEL)),
                ('current_classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='academics.classroom')),
                ('current_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='academics.academiclevel')),
            ],
            options={'ordering': ('admission_number',)},
        ),
        migrations.CreateModel(
            name='GuardianRelationship',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('relationship', models.CharField(choices=[('parent', 'Parent'), ('guardian', 'Guardian')], max_length=32)),
                ('is_primary', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('guardian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guardian_relationships', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guardian_relationships', to='students.studentprofile')),
            ],
            options={'unique_together': {('student', 'guardian', 'relationship')}},
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='guardians',
            field=models.ManyToManyField(related_name='wards', through='students.GuardianRelationship', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='EnrollmentRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('academic_year', models.CharField(max_length=32)),
                ('term', models.CharField(max_length=32)),
                ('is_promoted', models.BooleanField(default=False)),
                ('registered_on', models.DateField(default=django.utils.timezone.now)),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academics.classroom')),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='academics.academiclevel')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='students.studentprofile')),
            ],
            options={'ordering': ('-registered_on',), 'unique_together': {('student', 'academic_year', 'term')}},
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')], max_length=16)),
                ('remarks', models.TextField(blank=True)),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academics.classroom')),
                ('recorded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='students.studentprofile')),
            ],
            options={'ordering': ('-date',), 'unique_together': {('student', 'date')}},
        ),
        migrations.CreateModel(
            name='StudentSubjectRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('academic_year', models.CharField(max_length=32)),
                ('term', models.CharField(max_length=32)),
                ('continuous_assessment', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('exam_score', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('grade', models.CharField(blank=True, max_length=5)),
                ('remarks', models.CharField(blank=True, max_length=255)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_records', to='students.studentprofile')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.subject')),
            ],
            options={'unique_together': {('student', 'subject', 'academic_year', 'term')}},
        ),
        migrations.CreateModel(
            name='StudentTransferHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('from_school_schema', models.CharField(max_length=63)),
                ('to_school_schema', models.CharField(max_length=63)),
                ('completed_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('remarks', models.TextField(blank=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_history', to='students.studentprofile')),
                ('transfer_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenancy.studenttransferrequest')),
            ],
        ),
        migrations.CreateModel(
            name='StudentDocument',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('document_url', models.URLField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='students.studentprofile')),
            ],
        ),
    ]
