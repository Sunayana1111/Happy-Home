from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.register import UserRegisterView
from .views.user import UserViewSet
from .views.login import LoginView

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')


urlpatterns = [
    path('login/', LoginView.as_view(), name="user_login"),
    path('register/', UserRegisterView.as_view()),
] + router.urls
