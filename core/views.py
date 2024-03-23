from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import ApplyCareGivingSerializer, LabServiceSerializer, CareGiverSerializer
from .models import LabService, CareGiver


class LabServicesView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = LabService.objects.all()
    serializer_class = LabServiceSerializer


class CareGiverView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = CareGiver.objects.all()
    serializer_class = CareGiverSerializer


class CareGiverDetailView(RetrieveAPIView):
    permission_classes = [AllowAny, ]
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    queryset = CareGiver.objects.all()
    serializer_class = CareGiverSerializer


class ApplyCareGivingView(CreateAPIView):
    serializer_class = ApplyCareGivingSerializer
