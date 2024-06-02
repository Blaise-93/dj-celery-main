from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """enable a webscoket connection, and get the ability to connect to chatroom"""

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chatrooms_%s' % self.room_name

        # allows us to utilize the group add, and construct a new group
        await self.channel_layer.group_add(
               self.room_group_name, 
               self.channel_name # contains a pointer to the channel layer instance 
               #to the channel name that will reach a consumer. 
        )

        await self.accept()

    async def disconnect(self, close_code):

        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        # get message from the user
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # send to the group
        await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chatroom_message",
                    'message': message   
                }
        )

    
    async def chatroom_message(self, event):
        message = event['message'] # data collected from group send
        
        await self.send(text_data=json.dumps({
            # the `message` originates from the user typing in message input in a real-time
            'message':message

        }))

        await self.close()
    
    
