import json

from django.db.models import Q
from rest_framework.authtoken.models import Token
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

from .models import ChatRoom, ChatMessage

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

    def disconnect(self, code):
        if self.user:
            async_to_sync(self.channel_layer.group_discard)(
                self.user.username,
                self.channel_name
            )

    def receive(self, text_data=None, bytes_data=None):
        print(self.user)
        data = json.loads(text_data)
        room_uuid = data.get("room_uuid")
        receiver_un = data.get("user")
        text = data.get("text")
        sender = self.user
        receiver = User.objects.get(username=receiver_un)
        users = [sender.id, receiver.id]
        if room_uuid:
            room = ChatRoom.objects.filter(Q(participants__icontains=users) |
                                           Q(participants__icontains=reversed(users)), uuid=room_uuid)
            if room:
                room = room[0]
                ChatMessage.objects.create(room=room, user=sender, text=text)
            else:
                self.send(text_data=json.dumps({"message": "Invalid chat room"}))
                return
        else:
            room = ChatRoom.objects.filter(Q(participants__icontains=users) |
                                           Q(participants__icontains=reversed(users)))
            if room:
                room = room[0]
                ChatMessage.objects.create(room=room, user=sender, text=text)
            else:
                room = ChatRoom.objects.create(participants=users)
                ChatMessage.objects.create(room=room, user=sender, text=text)
        for user in [sender, receiver]:
            async_to_sync(self.channel_layer.group_send)(user.username,
                                                         {"room_uuid": room.uuid.hex, "text": text,
                                                          "type": "chat_text"})

    def chat_text(self, event):
        print("Here")
        room_uuid = event.get("room_uuid")
        text = event.get("text")
        self.send(text_data=json.dumps({"room_uuid": room_uuid, "text": text}))
