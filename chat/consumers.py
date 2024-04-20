import json

from django.db.models import Q
from django.templatetags.static import static
from rest_framework.authtoken.models import Token
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
# from django.contrib.sites.models import Site

from .models import ChatRoom, ChatMessage

User = get_user_model()

# current_site = Site.objects.get_current()
# current_domain = current_site.domain
# print(current_domain)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        byte_token = self.scope.get('query_string')
        headers = self.scope.get('headers')
        host = headers[0]
        host = host[1].decode('utf-8')
        print(host)
        scheme = "http" if host == "127.0.0.1:8000" else "https"
        self.host = host
        self.scheme = scheme
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
        print(data)
        room_uuid = data.get("room_uuid")
        text = data.get("text")
        sender = self.user
        if room_uuid:
            room = ChatRoom.objects.filter(uuid=room_uuid)
            if room:
                room = room[0]
                message = ChatMessage.objects.create(room=room, user=sender, text=text)
                users_qs = User.objects.filter(id__in=room.participants)
                receiver = users_qs.exclude(id__in=[sender.id])[0]
            else:
                self.send(text_data=json.dumps({"message": "Invalid chat room"}))
                return
        else:
            receiver_un = data.get("user")
            try:
                receiver = User.objects.get(username=receiver_un)
            except:
                self.send(text_data=json.dumps({"message": "Invalid username"}))
                return
            users = [sender.id, receiver.id]
            users_qs = User.objects.filter(id__in=users)
            room = ChatRoom.objects.filter(Q(participants__icontains=users) |
                                           Q(participants__icontains=reversed(users)))
            if room:
                room = room[0]
                message = ChatMessage.objects.create(room=room, user=sender, text=text)
            else:
                room = ChatRoom.objects.create(participants=users)
                message = ChatMessage.objects.create(room=room, user=sender, text=text)
        for user in users_qs:
            created_at = str(message.created_at)
            created_date = str(message.created_at.date())
            created_time = f"{message.created_at.time().hour}:{message.created_at.time().minute}"

            data = {"room_uuid": room.uuid.hex, "text": text, "type": "chat_text",
                    "sender": sender.username, "receiver": receiver.username, "created_at": created_at,
                    "created_date": created_date, "created_time": created_time}
            print(data)
            async_to_sync(self.channel_layer.group_send)(user.username, data)

    def chat_text(self, event):
        print("Here")
        room_uuid = event.get("room_uuid")
        text = event.get("text")
        receiver_un = event.get("receiver")
        sender = User.objects.get(username=event["sender"])
        receiver = User.objects.get(username=receiver_un)
        if event["sender"] == self.user.username:
            self_message = True
            user = self.user
        else:
            self_message = False
            user = receiver
        try:
            profile = user.userprofile
            if profile.profile_picture:
                image = f"{self.scheme}://{self.host}{profile.profile_picture.url}"
            else:
                image = f"{self.scheme}://{self.host}{static('chat/placeholder.webp')}"
        except:
            image = f"{self.scheme}://{self.host}{static('chat/placeholder.webp')}"

        data = {"room_uuid": room_uuid, "text": text, "self_message": self_message,
                                        "image": image, "sender_name": sender.first_name,
                                        "receiver_name": receiver.first_name}
        print(data)
        self.send(text_data=json.dumps(data))
