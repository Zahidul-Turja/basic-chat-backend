import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.services import *
from chat.serializers import *
from usermanager.models import *


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        if "user" in self.scope and "reciever_id" in self.scope:
            user = self.scope["user"]
            self.room_name = f"{user.name.lower()}_{user.id}"
        else:
            self.close()
            return

        sorted_ids = sorted(
            [str(self.scope["user"].id), str(self.scope["reciever_id"])]
        )
        self.room_group_name = f"group_of_{sorted_ids[0]}_{sorted_ids[1]}"
        print(self.room_group_name, self.room_name, "=====================")

        # Join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        print(f"{self.scope['user']} got disconnected.")

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender_id = str(self.scope["user"].id)
        receiver_id = str(self.scope["reciever_id"])

        text_data_json["sender_id"] = sender_id
        text_data_json["reciever_id"] = receiver_id

        # Process the incoming message
        data = create_message(**text_data_json)
        data = ConversationMessageSerializer(data).data

        sorted_ids = sorted([sender_id, receiver_id])
        user_room_name = f"group_of_{sorted_ids[0]}_{sorted_ids[1]}"

        print(text_data_json, "=====================")
        async_to_sync(self.channel_layer.group_send)(
            user_room_name,
            {"type": "chat_message", "response": data},
        )

    # Receive message from room group
    def chat_message(self, event):
        response = event["response"]

        # Send the message to WebSocket
        self.send(text_data=json.dumps(response))
