from rest_framework import serializers
from django.contrib.auth import get_user_model

from account.serializers.user import UserSerializer
from .models import ChatMessage

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
