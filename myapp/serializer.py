import random
from rest_framework import serializers
from rest_framework.views import set_rollback
from .models import *
from myapp import models

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = customer
        fields = "__all__"


class ProfileImageSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(queryset=customer.objects.all(), slug_field="mobile_number")

    class Meta:
        model = image_upload
        fields = "__all__"

class BooktradsmanSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(queryset=customer.objects.all(), slug_field="mobile_number")
    tradesman = serializers.SlugRelatedField(queryset=tradesman.objects.all(), slug_field="trade_id")

    def validate(self, data):
        tradesman_id = data['trade_id']
        tradesman = models.tradesman.objects.get(pk=tradesman_id)
        if tradesman.status != "active":
            raise serializers.ValidationError("tradesman is not active")
        
        return data

    class Meta:
        model = book_tradesman
        fields = "__all__"