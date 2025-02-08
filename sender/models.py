from django.db import models
from accounts.models import CustomUser

class SenderProfile(models.Model):
    pass

# Create your models here.
class SenderAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    def __str__(self):
        return self.address[:30]
