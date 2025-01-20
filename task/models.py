import datetime
from django.db import models
from accounts.models import CustomUser
from sender.models import SenderUser, SenderAddress
from courier.models import Courier


class Task(models.Model):
    PACKAGE_CATAGORY_CHOICES = (
        ('other', 'سایر'),
        ('food', 'غذا'),
        ('clothes', 'پوشاک'),
        ('home_devices', 'اساس منزل'),
        ('electronic_devices', 'لوازم برقی'),
        ('car_parts', 'قطعات خودرو'),
        ('cosmetics', 'شوینده و بهداشتی'),
        ('jwelery', 'زیورآلات'),
        ('paper', 'کاغذ و مدارک'),
    )
    STATUS_CHOICES = (
        ('pending', 'در انتظار'),
        ('accepted', 'پذیرفته شد'),
        ('in_transit', 'در حال ارسال'),
        ('delivered', 'تحویل داده شد'),
        ('canceled', 'کنسل شد'),
    )
    PAYMENT_TYPE_CHOICES = (
        ('prepay', 'پرداخت در مبدا'),
        ('postpay', 'پرداخت در مقصد')
    )
    VEHICLE_TYPE_CHOICES =(
        ('motor_without_box','موتور بدون باکس'),
        ('motor_with_box','موتور باکس دار'),
        ('sedan','سواری بار'),
        ('light_truck','وانت سبک'),
        ('truck','وانت'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    package_catagory = models.CharField(max_length=20, choices=PACKAGE_CATAGORY_CHOICES, default='other')
    sender = models.ForeignKey(SenderUser, on_delete=models.CASCADE, related_name="sourceuser", null=True)
    source_address = models.TextField()
    vehicle = models.CharField(max_length=20 , choices=VEHICLE_TYPE_CHOICES)
    destination_user_name = models.CharField(max_length=100)
    destination_address = models.TextField()
    destination_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    destination_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    distance_km = models.IntegerField(null=True, blank=True)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True)
    estimated_price = models.DecimalField(max_digits=10, decimal_places=0)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, null=False, blank=False , default='prepay')
    payed_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    request_time = models.DateTimeField(auto_now_add=True)
    courier_take_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    delivered = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    sender_note = models.TextField(null=True, blank=True)
    signal_note = models.TextField(null=True, blank=True)
    sender_request_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    sender_request_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return str(self.sender)


class TaskDeliveryLocation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location for Task {self.task.id} at {self.timestamp}"
