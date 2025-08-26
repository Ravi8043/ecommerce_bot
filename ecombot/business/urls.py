from rest_framework import routers
from django.urls import path, include
from . import views
from . import models
from . import serializers

router = routers.SimpleRouter()
router.register(r"businesses", views.BusinessViewSet, basename="business")

urlpatterns = [
    path('', include(router.urls)),
]