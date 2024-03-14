from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from ..serializers.user import UserSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
