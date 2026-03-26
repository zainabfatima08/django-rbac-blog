import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        print("WS USER:", self.scope["user"])


        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f"notifications_{self.user.id}"

        print("JOINING GROUP:", self.group_name)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        print("GROUP JOINED SUCCESSFULLY")

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        print(" MESSAGE RECEIVED IN CONSUMER:", event)

        await self.send(text_data=json.dumps({
            'id': event['id'],
            'message': event['message'],
            'notif_type': event['notif_type'],
            'post_slug': event['post_slug'],
            'created_at': event['created_at'],
        }))



