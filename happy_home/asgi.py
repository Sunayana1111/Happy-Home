import os
import django

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'happy_home.settings')
django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    "websocket": URLRouter(chat.routing.websocket_urlpatterns),
    "http": get_asgi_application(),
})

