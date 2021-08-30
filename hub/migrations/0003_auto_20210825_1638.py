# Generated by Django 3.2.4 on 2021-08-25 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hub', '0002_rename_structured_lease_payments_structuredleasepayments'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.PositiveIntegerField(choices=[(1, 1), (3, 3), (6, 6), (12, 12), (15, 15), (18, 18), (24, 24), (36, 36), (48, 48), (60, 60)])),
                ('rate_type', models.CharField(choices=[('Normal', 'Normal'), ('Senior Citizen', 'Senior Citizen')], max_length=20)),
                ('interest_payment', models.CharField(choices=[('Monthly', 'Monthly'), ('Maturity', 'Maturity')], max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='leaseapplication',
            name='vehicle_valuation',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='DepositRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest_rate', models.FloatField()),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('lender', models.ForeignKey(limit_choices_to={'groups__name': 'borrower'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hub.depositproduct')),
            ],
        ),
    ]