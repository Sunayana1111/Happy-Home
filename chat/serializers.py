from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from rest_framework import serializers
from django.contrib.auth import get_user_model
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
    self_message = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ["created_at",  "created_date", "created_time", "text", "self_message", "image", "name", "sender_name"]

    def get_self_message(self, obj):
        request = self.context.get("request")
        if request:
            return obj.user == request.user
        return False

    def get_created_date(self, message):
        return message.created_at.date()

    def get_created_time(self, message):
        return f"{message.created_at.time().hour}:{message.created_at.time().minute}"

    def get_image(self, message):
        user = message.user
        request = self.context.get("request")
        try:
            profile = user.userprofile
            if profile.profile_picture:
                return f"{request.scheme}://{get_current_site(request).domain}{profile.profile_picture.url}"
            return f"{request.scheme}://{get_current_site(request).domain}{static('chat/placeholder.webp')}"
        except:
            return f"{request.scheme}://{get_current_site(request).domain}{static('chat/placeholder.webp')}"

    def get_name(self, message):
        request = self.context.get("request")
        room = message.room
        users = User.objects.filter(id__in=room.participants).exclude(id=request.user.id)
        if users:
            return users[0].get_full_name()
        return "Chat Room"

    def get_sender_name(self, message):
        return message.user.first_name


class UserChatRoomSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    last_message_date = serializers.SerializerMethodField()
    uuid = serializers.SerializerMethodField()
    # username =

    class Meta:
        model = ChatRoom
        fields = ["uuid", "name", "image", "last_message", "last_message_date"]

    def get_uuid(self, room):
        return room.uuid.hex

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

    def get_last_message_date(self, room):
        message = ChatMessage.objects.filter(room=room)
        if message:
            message = message.latest("-created_at")
            return message.created_at.date()
        return None

    def get_image(self, room):
        request = self.context.get("request")
        return f"{request.scheme}://{get_current_site(request).domain}{static('chat/placeholder.webp')}"
