from rest_framework import serializers
from account.models import OTP


class ForgetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        otp = attrs["otp"]
        qs = OTP.objects.filter(digits=otp)
        if not qs.exists():
            raise serializers.ValidationError("Invalid OTP !")
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords didn't match")
        return attrs
