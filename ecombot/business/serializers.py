# business/serializers.py
from rest_framework import serializers
from .models import Business

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            "id",
            "owner",
            "business_name",
            "description",
            "instagram_handle",
            "website",
            "niche",
            "integrations",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "is_verified", "created_at", "updated_at"]

    def create(self, validated_data):
        user = self.context['request'].user
        return Business.objects.create(owner=user, **validated_data)