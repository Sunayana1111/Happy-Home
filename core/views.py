import requests
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from commons.utils import generate_random_key

from .serializers import CGAppointmentSerializer, LabServiceSerializer, CareGiverSerializer, CGTranxInitiateSer, \
TranxVerifySer
from .models import LabService, CareGiver, TransactionCGService, TransactionLabService
from .constants import KHALTI, INITIATED, UNVERIFIED, VERIFIED
from .khalti import KhaltiPayment


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


class CGBoookAppointmentView(CreateAPIView):
    serializer_class = CGAppointmentSerializer


class TranxInitiateView(CreateAPIView):
    serializer_class = CGTranxInitiateSer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=self.request.data)
        ser.is_valid(raise_exception=True)
        appointment = ser.validated_data['appointment']
        product_id = generate_random_key(alpha_numeric=True, size=8)

        create_data = dict(appointment=appointment, product_id=product_id, amount=10000, status=INITIATED)

        if ser.service == "Caregiver":
            product_name = "CareGiverAppointment"
            tranx = TransactionCGService.objects.create(**create_data)
        else:
            product_name = "LabServiceAppointment"
            tranx = TransactionLabService.objects.create(**create_data)
        return Response({
            "uuid": tranx.uuid,
            "product_id": tranx.product_id,
            "product_name": product_name,
            "product_url": "https://happyhome.com",
            "amount": tranx.amount,
            "message": "Transaction has been initiated"
        })



class TranxVerifyView(CreateAPIView):
    serializer_class = TranxVerifySer
    khalti = KhaltiPayment()
    khalti_headers = dict(Authorization=f"Key {khalti.secret_key}")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['khalti_token']
        transaction = serializer.validated_data['transaction_uuid']
        payload = dict(token=token, amount=transaction.amount)
        response = requests.request("POST", self.khalti.transaction_verify_url, headers=self.khalti_headers, data=payload)
        transaction.payment_medium = KHALTI
        if response.status_code == 200:
            transaction.status = VERIFIED
            transaction.is_paid = True
            message = "Your payment has been confirmed !!"
        else:
            transaction.status = UNVERIFIED
            message = "Invalid payment request !!"
        transaction.server_response = response.json()
        transaction.save()
        return Response({
            "message": message
        }, status=response.status_code)
