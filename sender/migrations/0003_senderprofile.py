# Generated by Django 5.1.5 on 2025-02-08 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0002_delete_senderuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='SenderProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
