from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import ApplyCareGivingSerializer


class LabServicesView(APIView):
    
    def get(self, request, *args, **kwargs):
        response = [
            {"id": 1, "name": "Blood Test"},
            {"id": 2, "name": "Urine Test"},
            {"id": 1, "name": "Cholestrol Test"},
            {"id": 1, "name": "Overall Body Test"},
            {"id": 1, "name": "COVID Test"},
        ]
        return Response(response)


class ApplyCareGivingView(CreateAPIView):
    serializer_class = ApplyCareGivingSerializer
