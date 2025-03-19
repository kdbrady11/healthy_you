# Generated by Django 5.1.7 on 2025-03-19 16:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], max_length=10)),
                ('start_date', models.DateField(help_text='The date when this medication regimen starts.')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MedicationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('taken', 'Taken'), ('not_taken', 'Not Taken'), ('not_recorded', 'Not Recorded')], default='not_recorded', max_length=15)),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medications.medication')),
            ],
            options={
                'unique_together': {('medication', 'date')},
            },
        ),
    ]
