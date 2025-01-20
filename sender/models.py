from django.db import models
from accounts.models import CustomUser


# Create your models here.
class SenderAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    def __str__(self):
        return self.address[:30]

class SenderUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    balance = models.IntegerField(default=0)
    deposite = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return str(self.user.first_name)