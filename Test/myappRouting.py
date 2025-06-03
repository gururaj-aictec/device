from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/ws/", consumers.my_websocket_consumer),
]

# 这里，consumers模块中的my_websocket_consumer是一个WebSocket处理器
