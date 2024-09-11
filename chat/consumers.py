import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        message_type = data.get('type', 'text')

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_type': message_type
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        message_type = event['message_type']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'type': message_type
        }))

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"call_{self.room_name}"

        # Join room group for calls
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        sdp = data.get('sdp')
        candidate = data.get('candidate')

        # Send SDP or ICE candidate to other peers in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_message',
                'sdp': sdp,
                'candidate': candidate
            }
        )

    async def call_message(self, event):
        sdp = event.get('sdp')
        candidate = event.get('candidate')

        # Forward the SDP or ICE candidate to the WebSocket
        await self.send(text_data=json.dumps({
            'sdp': sdp,
            'candidate': candidate
        }))
