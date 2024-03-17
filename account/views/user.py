from rest_framework.generics import ListAPIView
from ..serializers.user import UserSerializer

from django.contrib.auth.models import User


class UserView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
