# Generated by Django 3.2.4 on 2021-08-25 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaseApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('applicant_legal_first_name', models.CharField(max_length=200)),
                ('applicant_legal_last_name', models.CharField(max_length=200)),
                ('applicant_date_of_birth', models.DateField()),
                ('nic_number', models.CharField(max_length=12)),
                ('monthly_income', models.FloatField(default=0)),
                ('monthly_expenditure', models.FloatField(default=0)),
                ('vehicle_make', models.CharField(max_length=50)),
                ('vehicle_model', models.CharField(max_length=50)),
                ('vehicle_year', models.PositiveIntegerField()),
                ('vehicle_mileage', models.PositiveIntegerField()),
                ('vehicle_price', models.FloatField()),
                ('requiested_loan_amount', models.PositiveIntegerField()),
                ('preffered_term', models.PositiveIntegerField(blank=True, null=True)),
                ('date_loan_required', models.DateField()),
                ('first_year_max_rental', models.PositiveIntegerField(blank=True, null=True)),
                ('has_valuation', models.BooleanField(default=False)),
                ('vehicle_valuation', models.FloatField()),
                ('has_co_applicant', models.BooleanField(default=False)),
                ('co_applicant_first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('co_applicant_last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('co_applicant_nic_number', models.CharField(blank=True, max_length=12, null=True)),
                ('co_applicant_monthly_income', models.FloatField(blank=True, default=0, null=True)),
                ('has_guarantor', models.BooleanField(default=False)),
                ('guarantor_first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('guarantor_last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('guarantor_nic_number', models.CharField(blank=True, max_length=12, null=True)),
                ('application_expired', models.BooleanField(default=False)),
                ('comments', models.TextField(blank=True, null=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeaseContractOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_amount', models.PositiveIntegerField()),
                ('interest_rate', models.FloatField()),
                ('loan_term', models.PositiveIntegerField()),
                ('monthly_rental', models.FloatField(null=True)),
                ('documentation_fees', models.FloatField()),
                ('other_fees', models.FloatField(default=0)),
                ('stamp_duty', models.FloatField()),
                ('fees_included_in_loan_amount', models.BooleanField(default=False)),
                ('penalty_interest_rate', models.FloatField()),
                ('penalty_interest_after', models.PositiveIntegerField()),
                ('prepayment_rebate', models.FloatField(blank=True, null=True)),
                ('first_payment_in', models.CharField(choices=[('Immediate', 'Immediate'), ('In a month', 'In a month')], max_length=20)),
                ('structured_lease', models.BooleanField(default=False)),
                ('comments', models.TextField(blank=True, null=True)),
                ('LeaseApplication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hub.leaseapplication')),
                ('lender', models.ForeignKey(limit_choices_to={'groups__name': 'borrower'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Structured_lease_payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_month', models.PositiveIntegerField()),
                ('ending_month', models.PositiveIntegerField()),
                ('rental_amount', models.FloatField()),
                ('LeaseContractOffer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hub.leasecontractoffer')),
            ],
        ),
    ]
