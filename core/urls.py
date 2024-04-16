from django.urls import path
from core.views import LabServicesView, BoookAppointmentView, CareGiverView, CareGiverDetailView, \
    TranxInitiateView, TranxVerifyView, UserAppointments


urlpatterns = [
    path('lab-services/', LabServicesView.as_view()),
    path("appointment/transaction/initiate/", TranxInitiateView.as_view()),
    path("book-appointment/", BoookAppointmentView.as_view()),
    path("appointment/transaction/verify/", TranxVerifyView.as_view()),
    path("care-giver/", CareGiverView.as_view()),
    path("care-giver/<str:uuid>/", CareGiverDetailView.as_view()),
    path("uer-appointments/", UserAppointments.as_view())
]
