from flask import Flask, render_template
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.db import database_sync_to_async
import yourapp.routing  # 替换为您的应用路由模块
from django.urls import path
app = Flask(__name__)

# Flask的HTTP路由
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket路由
websocket_urlpatterns = [
    # 这里添加您的WebSocket URL路由
    path("ws/ws/", yourapp.routing.my_websocket_consumer),
]

# 创建WebSocket应用
websocket_application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

# 异步运行WebSocket应用
import asyncio
asyncio.run(database_sync_to_async(websocket_application))
