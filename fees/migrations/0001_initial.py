from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenancy', '0001_initial'),
        ('academics', '0001_initial'),
        ('students', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeStructure',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('is_independent', models.BooleanField(default=False)),
                ('applies_to_management_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenancy.managementgroup')),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('account_number', models.CharField(max_length=64)),
                ('bank_name', models.CharField(max_length=255)),
                ('level', models.CharField(choices=[('national', 'National'), ('region', 'Region'), ('district', 'District'), ('circuit', 'Circuit'), ('school', 'School'), ('group', 'Management Group')], max_length=32)),
                ('is_active', models.BooleanField(default=True)),
                ('administrative_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenancy.administrativeunit')),
                ('management_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenancy.managementgroup')),
            ],
        ),
        migrations.CreateModel(
            name='FeeComponent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('is_mandatory', models.BooleanField(default=True)),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='fees.feestructure')),
            ],
            options={'unique_together': {('structure', 'name')}},
        ),
        migrations.CreateModel(
            name='FeeSchedule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('academic_year', models.CharField(max_length=32)),
                ('term', models.CharField(max_length=32)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='fees.feecomponent')),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academics.academiclevel')),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='fees.feestructure')),
            ],
            options={'unique_together': {('structure', 'academic_year', 'term', 'component', 'level')}},
        ),
        migrations.CreateModel(
            name='DiscountPolicy',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('applies_to_component', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fees.feecomponent')),
                ('applies_to_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academics.academiclevel')),
            ],
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('start_year', models.CharField(max_length=32)),
                ('end_year', models.CharField(blank=True, max_length=32)),
                ('discount_policy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fees.discountpolicy')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scholarships', to='students.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('academic_year', models.CharField(max_length=32)),
                ('term', models.CharField(max_length=32)),
                ('status', models.CharField(choices=[('unpaid', 'Unpaid'), ('partial', 'Partially Paid'), ('paid', 'Paid')], default='unpaid', max_length=16)),
                ('issued_on', models.DateField(default=django.utils.timezone.now)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('structure', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fees.feestructure')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='students.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceLineItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('component', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fees.feecomponent')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_items', to='fees.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid_on', models.DateField(default=django.utils.timezone.now)),
                ('reference', models.CharField(blank=True, max_length=255)),
                ('bank_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fees.bankaccount')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='fees.invoice')),
                ('received_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentAllocation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('line_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='fees.invoicelineitem')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='fees.payment')),
            ],
        ),
    ]
