from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ('name',)},
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
                ('recommended_class_size', models.PositiveIntegerField(default=40)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='academics.programme')),
            ],
            options={'ordering': ('order',), 'unique_together': {('programme', 'name')}},
        ),
        migrations.CreateModel(
            name='AcademicLevel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levels', to='academics.section')),
            ],
            options={'ordering': ('order',), 'unique_together': {('section', 'name')}},
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=50)),
                ('workload_hours', models.PositiveIntegerField(default=1)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='academics.academiclevel')),
            ],
            options={'ordering': ('name',), 'unique_together': {('level', 'code')}},
        ),
        migrations.CreateModel(
            name='GradingScheme',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('min_score', models.PositiveIntegerField()),
                ('max_score', models.PositiveIntegerField()),
                ('grade', models.CharField(max_length=5)),
                ('remark', models.CharField(blank=True, max_length=255)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grading_schemes', to='academics.section')),
            ],
            options={'ordering': ('-min_score',)},
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('stream', models.CharField(blank=True, max_length=100)),
                ('capacity', models.PositiveIntegerField(default=40)),
                ('class_teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homeroom_classrooms', to=settings.AUTH_USER_MODEL)),
                ('coordinator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coordinated_classrooms', to=settings.AUTH_USER_MODEL)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='academics.academiclevel')),
            ],
            options={'ordering': ('level__order', 'name', 'stream'), 'unique_together': {('level', 'name', 'stream')}},
        ),
        migrations.CreateModel(
            name='SubjectAllocation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('weekly_periods', models.PositiveIntegerField(default=4)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_allocations', to='academics.classroom')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='academics.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_allocations', to=settings.AUTH_USER_MODEL)),
            ],
            options={'unique_together': {('classroom', 'subject')}},
        ),
        migrations.CreateModel(
            name='LessonPlan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('week_number', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('objectives', models.TextField()),
                ('resources', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_plans', to='academics.subject')),
            ],
            options={'ordering': ('subject', 'week_number'), 'unique_together': {('subject', 'week_number', 'title')}},
        ),
        migrations.CreateModel(
            name='SyllabusProgress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('completion_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('notes', models.TextField(blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lesson_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress_entries', to='academics.lessonplan')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ('updated_at',)},
        ),
    ]
