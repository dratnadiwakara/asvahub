# Generated by Django 3.2.4 on 2021-08-30 02:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0008_alter_depositoffer_depositinquiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Di',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inquirer_email', models.EmailField(max_length=254)),
                ('deposit_amount', models.PositiveIntegerField()),
                ('deposit_term', models.PositiveIntegerField()),
                ('inquiry_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Do',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offered_rate', models.FloatField()),
                ('offered_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('di', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='di', to='hub.di')),
            ],
        ),
    ]
