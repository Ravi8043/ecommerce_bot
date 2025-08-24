from django.db import models
from users.models import User

# Create your models here.
class Business(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='businesses')
    business_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    instagram_handle = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    niche = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#website integrations
    integrations = models.JSONField(blank=True, null=True)
    # shopify_token = models.CharField(max_length=255, blank=True, null=True)
    # woocommerce_key = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name