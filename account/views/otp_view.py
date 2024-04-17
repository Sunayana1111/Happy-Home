from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..serializers.otp_ser import OTPSerializer


class OTPView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "message": "An OTP has been sent to your email !"
        }, status=status.HTTP_200_OK, headers=headers)
