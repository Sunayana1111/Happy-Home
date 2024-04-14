from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.serializers.user import UserSerializer
from .models import ChatMessage, ChatRoom

User = get_user_model()


class RoomCheckSerializer(serializers.Serializer):
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())


class FirstMessageSerializer(serializers.Serializer):
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    text = serializers.CharField()


class RoomMessageSerializer(serializers.Serializer):
    text = serializers.CharField()


class RoomMessageListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    self_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ["created_at", "user", "text", "self_message"]

    def get_self_message(self, obj):
        request = self.context.get("request")
        if request:
            return obj.user == request.user
        return False


class UserChatRoomSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ["uuid", "name", "image", "last_message"]

    def get_name(self, room):
        request = self.context.get("request")
        users = User.objects.filter(id__in=room.participants).exclude(id=request.user.id)
        if users:
            return users[0].get_full_name()
        return "Chat Room"

    def get_last_message(self, room):
        message = ChatMessage.objects.filter(room=room)
        if message:
            message = message.latest("-created_at")
            return message.text
        return None

    def get_image(self, room):
        from django.templatetags.static import static
        from django.contrib.sites.shortcuts import get_current_site
        request = self.context.get("request")
        return f"{request.scheme}://{get_current_site(request).domain}{static('chat/placeholder.webp')}"
