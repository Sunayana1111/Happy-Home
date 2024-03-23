from django.contrib import admin
from .models import CareGiver, LabService, LabServiceAppointment, CareGiverAppointment, \
TransactionCGService, TransactionLabService


admin.site.register(CareGiver)
admin.site.register(LabService)
admin.site.register(LabServiceAppointment)
admin.site.register(CareGiverAppointment)
admin.site.register(TransactionCGService)
admin.site.register(TransactionLabService)
