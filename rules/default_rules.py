from kernel.interfaces.interfaces import InterfaceManager
from chatroom.rules.stack import CHATROOM_RULESTACK
import json
import pprint

class ChatRoomDefaultInterface(InterfaceManager):
    """
        @description: 
    """
    def event_init_consumer(
        self: object,
        consumer: object,
    ):
        """
            @description: Event declenched when the consumer is initialized.
            @params.consumer: The consumer to init.
        """
        from chatroom.models import ChatRoom
        dbProfile = consumer.scope.get('profile')
        if dbProfile is None:
            return

        dbChatroom = ChatRoom.objects.filter(onwer=dbProfile)
        chatroom_list = []
        for chatroom in dbChatroom:
            chatroom_list.append(chatroom.serialize())

        consumer.send(text_data=json.dumps({
            'init': {
                'chatroom_list': chatroom_list
            },
        }))

    def event_recept_message(
        self: object, 
        message: dict, 
        consumer: object
    ) -> None: 
        """
            @description: Event declenched when a message is recepted. 
            @params.message: The message to recept.
            @params.consumer: The consumer to recept the message.
            @return: void
        """
        pass

    def event_join_room(
            self: object, 
            consumer: object,
            chatroom__id: int, 
            user__id: int,
        ):
        """
            @description: Event declenched when a user join a room.
            @params.consumer: The consumer to communicate with the use in websocket.
            @params.room_name: The name of the room to join.
            @params.user__id: The id of the user who join the room.
        """
        from chatroom.models import ChatRoom
        from profiles.models import Profile
        from chatroom.managers.chat_room import CHATROOM_MANAGER
        dbProfile = Profile.objects.filter(user__id=user__id).first()
        if dbProfile is None:
            return
        
        dbChatroom = ChatRoom.objects.filter(
            id=chatroom__id, 
            onwer=dbProfile
        ).first()

        if dbChatroom is None:
            return
        # TODO: Add the disconnect message. 
        consumer.scope['USERINCHAT'] = CHATROOM_MANAGER.connect(dbChatroom, consumer)

    def event_before_delete_chatroom(
        self: object, 
        consumer: object,
        dbRoom: object,
        dbProfile: object,
    ):
        """
            @description: Runned before delete a room.
            @params.consumer: The consumer to communicate with the use in websocket.
            @params.dbRoom: The room to delete.
            @params.dbProfile: The profile who delete the room. 
        """
        
    def event_after_delete_chatroom(
        self: object, 
        consumer: object,
        dbRoom: object,
        dbProfile: object,
    ):
        """
            @description: Runned before delete a room.
            @params.consumer: The consumer to communicate with the use in websocket.
            @params.dbRoom: The room to delete.
            @params.dbProfile: The profile who delete the room.
        """



CHATROOM_RULESTACK.set_rule(ChatRoomDefaultInterface())