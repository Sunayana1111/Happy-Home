from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from .serializers import RoomCheckSerializer, FirstMessageSerializer, RoomMessageSerializer, \
    RoomMessageListSerializer
from .models import ChatRoom, ChatMessage


class RoomCheckView(CreateAPIView):
    serializer_class = RoomCheckSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, context={"request": self.request})
        ser.is_valid(raise_exception=True)
        another_user = ser.validated_data["user"]
        users = [self.request.user.id, another_user.id]
        room = ChatRoom.objects.filter(participants__icontains=users)
        if room.exists():
            room_uuid = room[0].uuid.hex
        else:
            room_uuid = None
        return Response({
            "room_uuid": room_uuid,
            "room_name": another_user.get_full_name() if another_user.get_full_name() else
            another_user.username.title(),
            "room_exists": True if room_uuid else False
        })


class FirstMessageView(CreateAPIView):
    serializer_class = FirstMessageSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        users = [ser.validated_data["user"].id, self.request.user.id]
        room = ChatRoom.objects.filter(Q(participants__icontains=users) |
                                       Q(participants__icontains=reversed(users)))
        if room.exists():
            return Response({
                "message": "Room already exists !"
            }, status=status.HTTP_400_BAD_REQUEST)
        room = ChatRoom.objects.create(participants=users)
        text = ser.validated_data["text"]
        ChatMessage.objects.create(room=room, text=text, user=self.request.user)
        return Response({
            "text": text,
            "room_uuid": room.uuid
        }, status=status.HTTP_201_CREATED)


class RoomMessageCreateView(CreateAPIView):
    serializer_class = RoomMessageSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"

    def get_queryset(self):
        return ChatRoom.objects.filter(participants__icontains=self.request.user.id)

    def create(self, request, *args, **kwargs):
        room = self.get_object()
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        text = ser.validated_data["text"]
        ChatMessage.objects.create(room=room, text=text, user=self.request.user)
        return Response({
            "text": text,
        }, status=status.HTTP_201_CREATED)


class RoomMessageListView(ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = RoomMessageListSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"

    def get_queryset(self):
        return ChatRoom.objects.filter(participants__icontains=self.request.user.id)

    def list(self, request, *args, **kwargs):
        room = self.get_object()
        messages = ChatMessage.objects.filter(room=room)
        queryset = self.filter_queryset(messages)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)
