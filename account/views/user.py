from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from commons.viewsets import ListRetrieveUpdateViewSet
from ..serializers.user import UserSerializer


@method_decorator(csrf_exempt, name='update')
class UserViewSet(ListRetrieveUpdateViewSet):
    lookup_field = "username"
    lookup_url_kwarg = "username"
    serializer_class = UserSerializer
    queryset = User.objects.all()
