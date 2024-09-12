from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add or override fields if needed
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Use a unique related name
        blank=True,
        help_text=('The groups this user belongs to. '
                   'A user will get all permissions granted to each of their groups.'),
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Use a unique related name
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name='customuser',
    )





