from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('tenancy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicCalendar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('academic_year', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('management_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic_calendars', to='tenancy.managementgroup')),
            ],
            options={'unique_together': {('management_group', 'academic_year')}},
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('scope', models.CharField(default='national', max_length=64)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holidays', to='calendars.academiccalendar')),
            ],
            options={'ordering': ('date',)},
        ),
        migrations.CreateModel(
            name='AcademicTerm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('registration_start', models.DateField(blank=True, null=True)),
                ('registration_end', models.DateField(blank=True, null=True)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='calendars.academiccalendar')),
            ],
            options={'ordering': ('start_date',)},
        ),
        migrations.CreateModel(
            name='EventBooking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('location', models.CharField(blank=True, max_length=255)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_bookings', to='calendars.academiccalendar')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.user')),
            ],
        ),
    ]
