from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include("dashboard.urls")),
    path('api/', include('api.urls'))
]


if settings.DEBUG:
    from api.swagger import SwaggerSchemaView
    from django.views.generic import RedirectView

    urlpatterns += [
        path('api/root/', SwaggerSchemaView.as_view()),
        path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
        path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    ]
    from django.shortcuts import render

    def chat_test(r):
        return render(r, template_name='socket/test.html')

    urlpatterns += [
        path('chat/test/', chat_test)
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
