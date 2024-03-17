from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views.register import UserRegisterView
from .views.user import UserView


urlpatterns = [
    path('login/', obtain_auth_token, name="user_login"),
    path('register/', UserRegisterView.as_view()),
    path("user/", UserView.as_view())
]
