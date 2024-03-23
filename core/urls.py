from django.urls import path
from core.views import LabServicesView, ApplyCareGivingView, CareGiverView, CareGiverDetailView

urlpatterns = [
    path('lab-services/', LabServicesView.as_view()),
    path("care-giver/", CareGiverView.as_view()),
    path("care-giver/<str:uuid>/", CareGiverDetailView.as_view()),
    path("apply-care-giving/", ApplyCareGivingView.as_view())
]
