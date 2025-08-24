from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique = True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_business = models.BooleanField(default = False)