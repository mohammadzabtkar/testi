# Generated by Django 5.1.5 on 2025-01-30 17:05

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
            name='Courier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('vehicle_type', models.CharField(choices=[('motor_without_box', 'موتور بدون باکس'), ('motor_with_box', 'موتور باکس دار'), ('sedan', 'سواری بار'), ('light_truck', 'وانت سبک'), ('truck', 'وانت')], max_length=20)),
                ('vehicle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('vehicle_country_number', models.IntegerField(blank=True, null=True)),
                ('vehicle_first_number', models.IntegerField(blank=True, null=True)),
                ('vehicle_alphabet', models.CharField(blank=True, max_length=1, null=True)),
                ('vehicle_second_number', models.IntegerField(blank=True, null=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('star', models.IntegerField(default=0)),
                ('balance', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('status', models.CharField(choices=[('online', 'online'), ('offline', 'offline'), ('at_work', 'at_work')], default='offline', max_length=10)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourierLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courier.courier')),
            ],
        ),
    ]
