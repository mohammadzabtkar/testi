# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
# class CustomUser(AbstractUser):
#     phone_number = models.CharField(max_length=15, null=True)
#     balance = models.IntegerField(default=0)
#     deposite = models.PositiveSmallIntegerField(default=0)
#
#     def __str__(self):
#         return self.username
#


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    balance = models.IntegerField(default=0)
    deposite = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.phone_number if self.phone_number else self.username
