from django.db import models
from accounts.models import CustomUser
from courier.models import Courier


class Task(models.Model):
    PACKAGE_CATEGORY_CHOICES = (
        ('other', 'سایر'),
        ('food', 'غذا'),
        ('clothes', 'پوشاک'),
        ('home_devices', 'اساس منزل'),
        ('electronic_devices', 'لوازم برقی'),
        ('car_parts', 'قطعات خودرو'),
        ('cosmetics', 'شوینده و بهداشتی'),
        ('jewelry', 'زیورآلات'),
        ('paper', 'کاغذ و مدارک'),
    )
    STATUS_CHOICES = (
        ('pending', 'در انتظار'),
        ('accepted', 'پذیرفته شد'),
        # ('in_transit', 'در حال ارسال'),
        ('delivered', 'تحویل داده شد'),
        ('canceled', 'کنسل شد'),
    )
    PAYMENT_SIDE_CHOICES = (
        ('source_pay', 'پرداخت توسط فرستنده'),
        ('destination_pay', 'پرداخت توسط گیرنده')
    )
    PAID_REPOSITORY_CHOICES = (
        ('online','پرداخت آنلاین'),
        ('wallet','پرداخت از کیف پول'),
    )
    VEHICLE_TYPE_CHOICES = (
        ('motor_without_box', 'موتور بدون باکس'),
        ('motor_with_box', 'موتور باکس دار'),
        ('sedan', 'سواری بار'),
        ('light_truck', 'وانت سبک'),
        ('truck', 'وانت نیسان'),
    )

    # Package Information
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    package_category = models.CharField(max_length=20, choices=PACKAGE_CATEGORY_CHOICES, default='other')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES ,default='motor_without_box')
    package_note = models.TextField(null=True, blank=True)  # یادداشت مشتری درباره بسته

    # Sender Information
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks", null=True)
    source_address = models.TextField()
    source_address_latitude = models.DecimalField(max_digits=9, decimal_places=6,default=0)
    source_address_longitude = models.DecimalField(max_digits=9, decimal_places=6,default=0)

    # Destination Information
    destination_user_name = models.CharField(max_length=100)
    destination_address = models.TextField()
    destination_address_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    destination_address_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    distance_km = models.IntegerField(null=False, default=0)
    estimated_price = models.DecimalField(max_digits=10, decimal_places=0)

    # Courier Information
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True)

    # Payment Information
    payment_side = models.CharField(max_length=20, choices=PAYMENT_SIDE_CHOICES, default='source_pay')
    paid_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    paid_repository = models.CharField(max_length=20, choices=PAID_REPOSITORY_CHOICES,null=True, blank=True)

    # Time Information
    request_time = models.DateTimeField(auto_now_add=True)
    courier_take_time = models.DateTimeField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True, blank=True)

    # def __str__(self):
    #     return f"Task {self.id} - {self.status}"


class PackageImage(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="task_packages/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Task {self.task.id} - {self.uploaded_at}"


class TaskDeliveryLocation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="locations")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location for Task {self.task.id} at {self.timestamp}"
