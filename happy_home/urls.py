from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]


if settings.DEBUG:
    from api.swagger import SwaggerSchemaView
    from django.views.generic import RedirectView

    urlpatterns += [
        path('api/root/', SwaggerSchemaView.as_view()),
        path('', RedirectView.as_view(url='/api/root/', permanent=False)),
        path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    ]
