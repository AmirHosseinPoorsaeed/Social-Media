from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path('ws/chat/<str:room_id>/', consumers.ChatRoomConsumer.as_asgi()),
]
