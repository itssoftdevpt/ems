from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenancy', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('target_level', models.CharField(choices=[('national', 'National'), ('region', 'Region'), ('district', 'District'), ('circuit', 'Circuit'), ('school', 'School'), ('classroom', 'Classroom')], max_length=32)),
                ('classroom_id', models.UUIDField(blank=True, null=True)),
                ('audience_roles', models.JSONField(blank=True, default=list)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('target_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenancy.administrativeunit')),
            ],
            options={'ordering': ('-created_at',)},
        ),
        migrations.CreateModel(
            name='MessageThread',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_threads', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(related_name='message_threads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('read_by', models.ManyToManyField(blank=True, related_name='read_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='communications.messagethread')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationPreference',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sms_enabled', models.BooleanField(default=False)),
                ('email_enabled', models.BooleanField(default=True)),
                ('push_enabled', models.BooleanField(default=True)),
                ('whatsapp_enabled', models.BooleanField(default=False)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notification_preference', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('notify_participants', models.BooleanField(default=True)),
                ('scope', models.CharField(choices=[('national', 'National'), ('region', 'Region'), ('district', 'District'), ('circuit', 'Circuit'), ('school', 'School')], max_length=32)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('scope_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenancy.administrativeunit')),
            ],
        ),
        migrations.CreateModel(
            name='EventNotification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('channel', models.CharField(default='email', max_length=32)),
                ('status', models.CharField(default='sent', max_length=32)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='communications.calendarevent')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
