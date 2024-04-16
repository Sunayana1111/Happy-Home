import requests
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from commons.utils import generate_random_key, send_template_email

from .serializers import BookAppointmentSerializer, LabServiceSerializer, CareGiverSerializer, CGTranxInitiateSer, \
    TranxVerifySer, LabAppointmentSerializer, CGAppointmentSerializer
from .models import LabService, CareGiver, TransactionCGService, \
    TransactionLabService, CareGiverAppointment, LabServiceAppointment
from .constants import KHALTI, INITIATED, UNVERIFIED, VERIFIED, CASH
from .khalti import KhaltiPayment


class LabServicesView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = LabService.objects.all()
    serializer_class = LabServiceSerializer


class CareGiverView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = CareGiver.objects.all()
    serializer_class = CareGiverSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CareGiverDetailView(RetrieveAPIView):
    permission_classes = [AllowAny, ]
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    queryset = CareGiver.objects.all()
    serializer_class = CareGiverSerializer


class BoookAppointmentView(CreateAPIView):
    serializer_class = BookAppointmentSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        appointment_for = ser.validated_data['appointment_for']
        full_name = ser.validated_data['full_name']
        phone = ser.validated_data['phone']
        address = ser.validated_data['address']
        start_date = ser.validated_data.get("start_date")
        end_date = ser.validated_data.get("end_date")
        description = ser.validated_data.get("description")
        payment_medium = ser.validated_data.get("payment_medium")

        product_id = generate_random_key(alpha_numeric=True, size=8)
        if ser.appt_for == "Caregiver":
            appt = CareGiverAppointment.objects.create(caregiver=appointment_for, service=description,
                                                       full_name=full_name,
                                                       phone=phone, address=address, start_date=start_date,
                                                       end_date=end_date, user=self.request.user)
            create_tranx_data = dict(appointment=appt, product_id=product_id, amount=10000, status=INITIATED)
            tranx = TransactionCGService.objects.create(payment_medium=payment_medium, **create_tranx_data)
            product_name = "CaregiverAppointment"
        else:
            appt = LabServiceAppointment.objects.create(user=request.user, service=appointment_for, full_name=full_name,
                                                        phone=phone, address=address, on_date=start_date)
            create_tranx_data = dict(appointment=appt, product_id=product_id, amount=10000, status=INITIATED)
            tranx = TransactionLabService.objects.create(payment_medium=payment_medium, **create_tranx_data)
            product_name = "LabserviceAppointment"
        tranx_response = {"transaction_uuid": tranx.uuid,
                          "payment_medium": payment_medium,
                          "product_id": tranx.product_id,
                          "product_name": product_name,
                          "product_url": "https://happyhome.com",
                          "amount": tranx.amount,
                          "message": "Transaction has been initiated"
                          }

        if payment_medium == CASH:
            send_mail(subject="Appointment Confirmation", message="You have successfully booked your "
                                                                  "Appointment", from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[settings.TO_EMAIL])

        return Response({
            "message": "Appointment booked successfully !!",
            "appointment_uuid": appt.uuid,
            "transaction": tranx_response
        }, status=status.HTTP_201_CREATED)


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
        response = requests.request("POST", self.khalti.transaction_verify_url, headers=self.khalti_headers,
                                    data=payload)
        transaction.payment_medium = KHALTI
        if response.status_code == 200:
            transaction.status = VERIFIED
            appointment = transaction.appointment
            appointment.is_paid = True
            appointment.save()
            message = "Your payment has been confirmed !!"
        else:
            transaction.status = UNVERIFIED
            message = "Invalid payment request !!"
        transaction.server_response = response.json()
        transaction.save()
        context = {
            "service": serializer.service.title(),
            "product_id": transaction.product_id,
            "payment_medium": transaction.payment_medium,
            "amount": transaction.amount / 100,
            "user": request.user,
            "date": transaction.created_at
        }
        send_template_email(request.user, subject="Appointment", context=context)
        return Response({
            "message": message
        }, status=response.status_code)


class UserAppointments(ListAPIView):
    def list(self, request, *args, **kwargs):
        lab_appointments = LabServiceAppointment.objects.filter(user=self.request.user)
        lab_Ser = LabAppointmentSerializer(lab_appointments, many=True, context={"request": self.request})
        cg_appointments = CareGiverAppointment.objects.filter(user=self.request.user)
        cg_ser = CGAppointmentSerializer(cg_appointments, many=True, context={"request": self.request})
        response = list(lab_Ser.data)
        response.extend(list(cg_ser.data))

        page = self.paginate_queryset(response)
        if page is not None:
            return self.get_paginated_response(page)
        return Response(response)
