# Generated by Django 5.1.5 on 2025-02-08 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courier',
            name='phone_number',
        ),
    ]
