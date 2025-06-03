import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MyWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        # 处理接收到的消息
        message = json.loads(text_data)
        # ...处理消息...
        response = {
            "message": message,
            "success": True
        }
        await self.send(text_data=json.dumps(response))
