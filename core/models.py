from django.db import models
from commons.models import BaseModel
from django.contrib.auth.models import User

from .constants import PAYMENT_MEDIUMS, TRANSACTION_STATUSES, INITIATED



class CareGiver(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="care_givers")
    speciality = models.CharField(max_length=200)
    languages = models.CharField(max_length=200)
    ratings = models.FloatField(null=True, blank=True)
    experience = models.CharField(max_length=50)  # in years/month
    bio = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Caregiver {self.user.username}"
    

class LabService(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class CareGiverAppointment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cg_appointments")
    caregiver = models.ForeignKey(CareGiver, on_delete=models.CASCADE, related_name="cg_appointments")
    service = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"CG Appointment By {self.user.username}"
    

class LabServiceAppointment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_lab_appointments")
    service = models.ForeignKey(LabService, on_delete=models.CASCADE, related_name='lab_appointments')
    lab_tech_name = models.CharField(max_length=100, null=True, blank=True)
    on_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Lab  Appointment By {self.user.username}"
    


class TransactionCGService(BaseModel):
    appointment = models.ForeignKey(CareGiverAppointment, on_delete=models.CASCADE, related_name='appointment_cg_tranx')
    amount = models.FloatField()  # in paisa
    product_id = models.CharField(max_length=100, unique=True)
    payment_medium = models.CharField(max_length=50, choices=PAYMENT_MEDIUMS, null=True, blank=True)
    status = models.CharField(max_length=50, default=INITIATED, choices=TRANSACTION_STATUSES)
    server_response = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"txn CG {self.product_id}"


class TransactionLabService(BaseModel):
    appointment = models.ForeignKey(LabServiceAppointment, on_delete=models.CASCADE, related_name='appointment_lab_tranx')
    amount = models.FloatField()  # in paisa
    product_id = models.CharField(max_length=100, unique=True)
    payment_medium = models.CharField(max_length=50, choices=PAYMENT_MEDIUMS, null=True, blank=True)
    status = models.CharField(max_length=50, default=INITIATED, choices=TRANSACTION_STATUSES)
    server_response = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"txn lab {self.product_id}"
