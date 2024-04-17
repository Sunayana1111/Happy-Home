from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from account.models import OTP
from ..serializers.forget_password_ser import ForgetPasswordSerializer


class PasswordResetView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ForgetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['new_password']
        otp = OTP.objects.get(digits=serializer.validated_data["otp"])
        email = otp.email
        otp.delete()
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return Response({
            "message": "Your password has been reset !"
        })
