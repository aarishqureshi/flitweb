from enum import auto
from django.db import models
from django.db.models.base import Model, ModelStateFieldsCacheDescriptor

# Create your models here.

class temp_user(models.Model):
    mobile_number = models.CharField(max_length=14)
    otp = models.CharField(max_length=6)
    expiry_time = models.TimeField()
    create_time = models.TimeField(auto_now=True)

class customer(models.Model):
    customer_name = models.CharField(max_length=30)
    DOB = models.DateField(null=True, blank=True)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=14)
    status = models.CharField(max_length=20, choices=(("active","Active"),("inactive","Inactive")))
    created_date = models.DateField(auto_now=True)

    
class trade_type(models.Model):
    trade_id = models.IntegerField()
    trade_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=(("active","Active"),("inactive","Inactive")))

class tradesman(models.Model):
    tradesman_name = models.CharField(max_length=30)
    trade_type = models.ForeignKey(trade_type, on_delete=models.CASCADE, related_name="tradesman_trade_type")
    created_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=20, choices=(("active","Active"),("inactive","Inactive")))


class book_tradesman(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE, related_name="book_tradesman_customer")
    tradesman = models.ForeignKey(tradesman, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=40, choices=(("pending","Pending"),("booked","Booked"),("canceled","Canceled")))

class image_upload(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE, related_name="customer_image")
    image = models.ImageField(upload_to='uploads/')
    created_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=40, choices=(("active","Active"),("inactive","Inactive")), default='active')
