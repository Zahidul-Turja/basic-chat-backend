from django.urls import re_path, path

from chat.consumers import ChatConsumer

from live_chat_backend.middlewares import UserMiddleware

websocket_urlpatterns = [
    re_path("ws/chat/", UserMiddleware(ChatConsumer.as_asgi())),
]
