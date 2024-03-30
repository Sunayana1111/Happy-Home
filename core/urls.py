from django.urls import path, include
from core.views import LabServicesView, BoookAppointmentView, CareGiverView, CareGiverDetailView, \
TranxInitiateView, TranxVerifyView

caregiver_urls = [
    path("<str:uuid>/", CareGiverDetailView.as_view()),
    path("", CareGiverView.as_view()),
]

urlpatterns = [
    path('lab-services/', LabServicesView.as_view()),
    path("appointment/transaction/initiate/", TranxInitiateView.as_view()),
    path("book-appointment/", BoookAppointmentView.as_view()),
    path("appointment/transaction/verify/", TranxVerifyView.as_view()),
    path("care-giver/", include(caregiver_urls))
]
