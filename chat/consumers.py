import json
from rest_framework.authtoken.models import Token
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        byte_token = self.scope.get('query_string')
        if byte_token:
            token = byte_token.decode('utf-8')
            auth = Token.objects.filter(key=token)
            if auth:
                self.user = auth[0].user
                user = self.user
                self.accept()
                # socket_auth.delete()  # socket auth token for one time connection only
                async_to_sync(self.channel_layer.group_add)(
                    str(user.username),
                    self.channel_name
                )
                print("Web socket connected")
            else:
                print("Invalid auth")
        else:
            print("Auth not provided")
