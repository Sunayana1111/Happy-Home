import os
import binascii

from django.db import models
from django.contrib.auth import get_user_model
from commons.models import BaseModel

User = get_user_model()


class SocketAuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_socket_token')
    token = models.TextField(unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(40)).decode()


class ChatRoom(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    participants = models.JSONField(default=list)


class ChatMessage(BaseModel):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="room_messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_messages")
    text = models.TextField()
