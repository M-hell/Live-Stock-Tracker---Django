import json
from channels.generic.websocket import AsyncWebsocketConsumer


TRIGGER_GROUP_NAME = 'asgi_group'
STOCKS_GROUP_NAME = 'stocks_group'


class AsgiConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(TRIGGER_GROUP_NAME, self.channel_name)
        await self.channel_layer.group_add(STOCKS_GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(TRIGGER_GROUP_NAME, self.channel_name)
        await self.channel_layer.group_discard(STOCKS_GROUP_NAME, self.channel_name)

    # Called by group_send with type "asgi.trigger" '.' is replaced by '_' automatically
    async def asgi_trigger(self, event):
        await self.send(text_data=json.dumps({'type': 'asgi.trigger', 'id': event['id']}))

    async def stocks_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'type': 'stocks.update',
                    'stocks': event['stocks'],
                    'fetched_at': event['fetched_at'],
                }
            )
        )
