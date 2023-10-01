# chat/consumers.py
import json

from channels.generic.websocket import WebsocketConsumer
from chatroom.libs import load_last_100_message, serialize_messages_list
from chatroom.managers.chat_room import CHATROOM_MANAGER
from kernel.websocket.decorators import websocket__simplifier
from kernel.http.request import FakeRequest
from chatroom.models import ChatRoom


class ChatRoomConsumer(WebsocketConsumer):
    @websocket__simplifier
    def connect(self):
        self.accept()
        # self.init()

        room_name = self.scope['GET'].get('room')
        self.scope['USERINCHAT'] = CHATROOM_MANAGER.connect(room_name, self)

    def init(self):
        """
            @description:
        """
        messages = load_last_100_message()
        serialized_messages = serialize_messages_list(messages)
        self.send(text_data=json.dumps(serialized_messages))

    def disconnect(self, close_code):
        USERINCHAT = self.scope['USERINCHAT']
        USERINCHAT.room.disconnect(self)

    def receive(self, text_data):
        actions = json.loads(text_data)
        for action in actions:
            real_action_name = 'receive__' + action
            if not hasattr(self, real_action_name):
                self.send(text_data=json.dumps({
                    'error': 'Action not found: ' + real_action_name
                }))
                raise Exception('Action not found: ' + real_action_name)
            getattr(self, real_action_name)(actions[action])

    def receive__new_message(self, message):
        """
            @description:
        """
        USERINCHAT = self.scope['USERINCHAT']
        new_message = USERINCHAT.room.create_new_message(USERINCHAT.profile, message)
        USERINCHAT.room.send_allpeople({
            'new_message': new_message
        })

    def receive__init(self, message):
        """
            @description: Init.
        """