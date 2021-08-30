# Generated by Django 3.2.4 on 2021-08-27 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hub', '0004_auto_20210826_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offered_rate', models.FloatField()),
                ('offered_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('depositinquiry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hub.depositinquiry')),
                ('lender', models.ForeignKey(limit_choices_to={'groups__name': 'borrower'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]