# Generated by Django 5.1.7 on 2025-03-19 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthmetric',
            name='date',
            field=models.DateField(help_text='Select the date for these metrics'),
        ),
    ]
