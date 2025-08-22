from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique = True)
    phone_number = models.IntegerField()
    address = models.TextField()
    instagram_handle = models.CharField(max_length=255, blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    niche = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#website integrations
    shopify_token = models.CharField(max_length=255, blank=True, null=True)
    woocommerce_key = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name