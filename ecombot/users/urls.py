from django.urls import path, include

urlpatterns = [
    path('', include('dj_rest_auth.urls')),         # login, logout, password reset
    path('registration/', include('dj_rest_auth.registration.urls')),  # signup
]