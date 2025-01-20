from django.db import models
from accounts.models import CustomUser


class Courier(models.Model):
    STATUS_CHOICES =(
        ('online','online'),
        ('offline','offline'),
        ('at_work','at_work'),
    )
    VEHICLE_TYPE_CHOICES =(
        ('motor_without_box','موتور بدون باکس'),
        ('motor_with_box','موتور باکس دار'),
        ('sedan','سواری بار'),
        ('light_truck','وانت سبک'),
        ('truck','وانت'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    vehicle_type = models.CharField(max_length=20 , choices=VEHICLE_TYPE_CHOICES)
    vehicle_name = models.CharField(max_length=30 , blank=True , null=True )
    vehicle_country_number = models.IntegerField( blank=True , null=True)
    vehicle_first_number = models.IntegerField( blank=True , null=True)
    vehicle_alphabet = models.CharField(max_length=1 , blank=True , null=True)
    vehicle_second_number = models.IntegerField( blank=True , null=True)
    modify_time = models.DateTimeField(auto_now=True)
    star = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    status = models.CharField(max_length=10 , choices=STATUS_CHOICES , default='offline')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True) #برخی موارد میشه لوکیشن پیک رو ثبت کرد مثلا موقعی که آنلاین میشه
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.user.first_name

class CourierLocation(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location for Task {self.task.id} at {self.timestamp}"

