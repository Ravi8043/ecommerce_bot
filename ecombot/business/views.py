from django.shortcuts import render
from . import models
from . import serializers
from rest_framework import viewsets, permissions

# Create your views here.

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = models.Business.objects.all()
    serializer_class = serializers.BusinessSerializer