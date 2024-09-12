import datetime

from django.db import models
from accounts.models import CustomUser
class PackageType(models.Model):
    name = models.CharField(max_length=100 , default="type0")

class StartCustomer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)


class Courier(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    vehicle_type = models.CharField(max_length=50, choices=[
        ('motorcycle_no_box', 'Motorcycle Without Box'),
        ('motorcycle_box', 'Motorcycle With Box'),
        ('sedan', 'Sedan'),
        ('light_truck', 'Light Truck'),
        ('heavy_truck', 'Heavy Truck')
    ], default="none")
    # creation_time = models.DateTimeField(auto_now_add=True , default=datetime.datetime.now())
    modify_time = models.DateTimeField(auto_now=True)
    star=models.IntegerField( max_length=1,default=0)
    balance=models.DecimalField(max_digits=10 , decimal_places=0 , default=0)






class EndCustomer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)


# Create your models here.
class Task(models.Model):
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),#
        ('accepted', 'Accepted'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    ], default='pending')
    package_type = models.ForeignKey(PackageType, on_delete=models.CASCADE)
    # image=models.ImageField()
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    pickup_address = models.CharField(max_length=255)
    dropoff_address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    start_customer=models.ForeignKey(StartCustomer, on_delete=models.CASCADE)
    courier=models.ForeignKey(Courier, on_delete=models.CASCADE)
    end_customer =models.ForeignKey(EndCustomer, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=[
        ('pickup', 'Payment at Pickup'),
        ('dropoff', 'Payment at Dropoff')
    ])
    request_time = models.DateTimeField(auto_now_add=True)
    courier_take_time = models.DateTimeField(auto_now_add=True)
    deliverd = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField()
    is_delivered =models.BooleanField()
    comment=models.TextField()
    signal_note = models.TextField




