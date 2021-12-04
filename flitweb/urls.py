"""flitweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('api/generate_otp/',GetOTPAPIView.as_view(), name='generate_otp'),
    path('api/login_singup/',LoginSingUpAPIView.as_view(),name='login_singup'),
    path('api/customer_profile', CustomerProfileAPIView.as_view(), name='customer_profile'),
    path('api/profile_upload',ProfileUploadAPIView.as_view(),name='profile_uplaod'),
    path('api/book_tradsman',BookTradesmanAPIView.as_view(),name='book_tradesman')
]
