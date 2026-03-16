import json
from channels.generic.websocket import AsyncWebsocketConsumer


GROUP_NAME = "asgi_group"


class AsgiConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(GROUP_NAME, self.channel_name)

    # Called by group_send with type "asgi.trigger"
    async def asgi_trigger(self, event):
        await self.send(text_data=json.dumps({"id": event["id"]}))
