from django.urls import path
from .views import RoomCheckView, FirstMessageView, RoomMessageCreateView,\
RoomMessageListView


urlpatterns = [
    path('room/check/', RoomCheckView.as_view()),
    path('first/message/', FirstMessageView.as_view()),
    path("room/<str:uuid>/message/", RoomMessageCreateView.as_view()),
    path("room/<str:uuid>/get-message/", RoomMessageListView.as_view()),
]
