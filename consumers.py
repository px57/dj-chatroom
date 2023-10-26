# chat/consumers.py
import json

from channels.generic.websocket import WebsocketConsumer
from chatroom.managers.chat_room import CHATROOM_MANAGER
from kernel.websocket.decorators import websocket__simplifier
from kernel.http.request import FakeRequest
from kernel.interfaces.decorators import load_interface
from chatroom.models import ChatRoom

from chatroom.models import ChatRoom

from chatroom.rules.stack import CHATROOM_RULESTACK


class ChatRoomConsumer(WebsocketConsumer):
    @websocket__simplifier
    @load_interface(CHATROOM_RULESTACK)
    def connect(self):
        self.accept()
        self.interface.event_init_consumer(self)

    def disconnect(self, close_code):
        """
            @description: 
        """
        if 'USERINCHAT' not in self.scope:
            return
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

    def receive__join_room(self, data):
        """
            @description:
            @param.data: {'name': 'aoeu', 'profile__id': 2}
        """ 
        chatroom__id = data.get('chatroom__id')
        user__id = data.get('user__id')    
        self.interface.event_join_room(
            self,
            chatroom__id, 
            user__id
        )

    def receive__new_message(self, message):
        """
            @description:
        """
        USERINCHAT = self.scope['USERINCHAT']
    
        new_message = USERINCHAT.room.create_new_message(
            USERINCHAT.profile, 
            message
        )

        USERINCHAT.room.send_allpeople({
            'new_message': new_message
        })

    def receive__init(self, message):
        """
            @description: Init.
        """

    def receive__create_personnal_room(self, message):
        """
            @description: Create a personnal room.
        """
        dbChatRoom = ChatRoom.objects.create(
            name=message.get('name'),
            onwer=self.scope.get('profile')
        )
        
        self.send(text_data=json.dumps({
            'new_room': dbChatRoom.serialize()
        }))

    def receive__delete_room(self, chatroom):
        """
            @description: 
        """
        dbProfile = self.scope.get('profile')
        dbChatRoomList = ChatRoom.objects.filter(
            id=chatroom.get('id'),
            onwer=dbProfile
        )
        if not dbChatRoomList.exists():
            return; 
        
        # INTERFACE>>>[BEFORE_DELETE_CHATROOM]
        self.interface.event_before_delete_chatroom(
            self,
            dbChatRoomList.first(),
            dbProfile,
        )

        dbChatRoomList.delete()

        # INTERFACE>>>[AFTER_DELETE_CHATROOM]
        self.interface.event_after_delete_chatroom(
            self,
            dbChatRoomList.first(),
            dbProfile,
        )