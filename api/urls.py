from django.urls import path, include


urlpatterns = [
    path('account/', include('account.urls')),
    path('core/', include('core.urls')),
    path("chat/", include("chat.urls"))
]
