from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.register import UserRegisterView
from .views.user import UserViewSet
from .views.login import LoginView
from .views.otp_view import OTPView
from .views.forget_password_view import PasswordResetView

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')


urlpatterns = [
    path('login/', LoginView.as_view(), name="user_login"),
    path('register/', UserRegisterView.as_view(), name="user_register"),
    path("forget-password/generate/otp/", OTPView.as_view()),
    path("forget-password/reset/", PasswordResetView.as_view()),
] + router.urls
