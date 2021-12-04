from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, generics, serializers
import math, random
from myapp import models
# from .models import temp_user
from datetime import date, datetime, timedelta
from twilio.rest import Client
from .serializer import CustomerSerializer, ProfileImageSerializer, BooktradsmanSerializer
from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def generateOTP(mobile_number) :
 
    # Declare a digits variable 
    # which stores all digits
    digits = str(mobile_number)
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP

class GetOTPAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        mobile_number = request.data.get("mobile_number")
        
        if mobile_number:
            temp_user = models.temp_user()
            temp_user.mobile_number = mobile_number
            otp = generateOTP(mobile_number)
            temp_user.otp = otp
            temp_user.created_time = datetime.time(datetime.now())
            temp_user.expiry_time = datetime.time(datetime.now()+timedelta(minutes=1))
            temp_user.save()
            client = Client("ACxxxxxxxxxxxx","zzzzzzzzzzzz")
            client.messages.create(to=str(mobile_number),from_="9057287344",body=otp)    
            return Response({"Status":"OTP Sent",
                            "Message":"Verification OTP Sent on the mobile number"})
        else:
            return Response({"Message":"mobile number is required"})

        
class LoginSingUpAPIView(generics.GenericAPIView):
    def post(self, request, *args,**kwargs):
        otp = request.data.pop("otp")
        mobile_number = request.data.get('mobile_number')
        temp_user = models.temp_user.objects.filter(mobile_number=mobile_number).order_by("-id")[0]
        expiry_time = temp_user[0].expiry_time
        current_time = datetime.time(datetime.now())
        # verify otp
        if current_time < expiry_time:
            if temp_user.otp == otp:
                if models.customer.objects.filter(mobile_number=mobile_number).exists():
                    user = User.objects.get(username=mobile_number)
                    token = RefreshToken.for_user(user)
                    return Response({"Status":"Old User",
                                    "Token":token})
                else:
                    serializer = CustomerSerializer(data=request.data)
                    serializer.save()
                    email = request.data.get("email")
                    user = User.objects.create_user(username=mobile_number,password=mobile_number+otp,email=email)
                    token = RefreshToken.for_user(user)
                    return Response({"Status":"New User",
                                    "Token":Token})

            else:
                return Response({"Message":"otp is not valid"})
        else:
                return Response({"Message":"otp time is exipre"})

class CustomerProfileAPIView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    querySet = models.customer.objects.all()
    serializers_class = CustomerSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"Status":"Get","Data":serializer.data})

class ProfileUploadAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProfileImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Status":"1005-Validations","Message":"Profile Image updated Successfully"})        

class BookTradesmanAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, requset):
        serializer = BooktradsmanSerializer(data=requset.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Status":"1004-Request","Message":"Request Added Successfully"})    

