import random
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from account.models import OTP


class OTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = OTP
        fields = ["email"]

    def create(self, validated_data):
        email = validated_data["email"]
        otp = str(random.randint(100000, 999999))
        user = User.objects.filter(email=email)
        if user:
            OTP.objects.create(email=email, digits=otp)
            send_mail(subject="Happy Home OTP",
                      message=f"Your OTP for password reset is {otp}",
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[settings.TO_EMAIL,
                                      "naween321@gmail.com", email])
        return validated_data
