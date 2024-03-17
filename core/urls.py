from django.urls import path
from core.views import LabServicesView, ApplyCareGivingView

urlpatterns = [
    path('lab-services/', LabServicesView.as_view()),
    path("apply-care-giving/", ApplyCareGivingView.as_view())
]
