
from kernel.interfaces.interfaces import InterfaceManager
from chatroom.rules.stack import CHATROOM_RULESTACK

class ChatRoomDefaultInterface(InterfaceManager):
    """
        @description: 
    """

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


CHATROOM_RULESTACK.add_rule(ChatRoomDefaultInterface())