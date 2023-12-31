
from chatroom.managers.user import ChatUser
from chatroom.libs import load_last_100_message, serialize_messages_list
from chatroom.models import Message
from kernel.http.request import FakeRequest

# burger
import ast
import json
from ia_workspace.tools.chat_ai_engine import AISemanticChat

class RoomManager:
    """
        @description: RoomManager class
    """

    def __init__(self, room: dict) -> None:
        """
            @description: constructor
        """
        self.room = room
        self.users_count = 0
        self.user_list = []
        print ('room', room['db'])
        self.messages = load_last_100_message(room['db'])
        self.ai_engine = AISemanticChat()

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ [FIND]
    def find_userindex_by_consumer(self, consumer):
        """
            @description: find user by consumer
        """
        for user in self.user_list:
            if user.consumer == consumer:
                return self.user_list.index(user)
        return None

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ [CONNECT]
    def connect(self, consumer) -> ChatUser:
        """
            @description: connect
        """
        userinchat = ChatUser(consumer, self)
        if len(self.user_list) <= 0 : self.user_list.append(userinchat)
        else: self.user_list[0] = userinchat

        self.users_count = 1

        userinchat.send_message({
            'messages': serialize_messages_list(self.messages),
        })

        # 
        self.send_allpeople({
            'participants_counter': self.users_count,
        })
        return userinchat


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ [DISCONNECT]
    def disconnect(self, consumer):
        """
            @description: disconnect
        """
        user_index = self.find_userindex_by_consumer(consumer)
        if user_index is not None:
            self.user_list.pop(user_index)
            self.users_count -= 1
            self.send_allpeople({ 'participants_counter': self.users_count })

    def send_allpeople(self, message: dict) -> None:
        """
            @description: send message
        """
        count = 0
        for user in self.user_list:
            count += 1
            print(f"Sending message to user {count}.")
            user.send_message(message)

    # def send_to_self(self, self_user, message: dict) -> None:
    #     """
    #         @description: send message
    #     """
    #     for user in self.user_list:
    #         user.send_message(message)


    def receive(self):
        """
            @description: receive message
        """
        pass
    
    def create_new_ai_message( self, profile, message, type ) :   
        """
            @description: RoomManager class
            @params : message = request from the client. Either :
                - a full string query : "What's up?" 
                - a selected suggestion as a string :
                    {
                        "file_id": 234223,
                        "page_num":  324,
                        "index": 37,
                        "paragraph": "paragraph example",
                        "text": "Le texte a afficher."
                    }
        """

        print("#"*40)
        print("---AI Message Generation---")
        print(f"message : {message}")

        ai_response = "There is an error with the reponse generation"
        response_type = 'new_message_ai'

        if type == 'new_message' : 
            ai_response = self.ai_engine.get_ai_response_from_general_query(message)

        elif type == 'new_message_user_ext':
            response_type = "new_message_ai_ext"
            parsed_message = json.loads(message)
            # print(f"json_parsed_message : {parsed_message}")

            if isinstance(parsed_message, dict):
                # print("---Expand Suggestion---")
                ai_response = self.ai_engine.get_ai_response_for_suggestion_expand(parsed_message)
            else:
                return "There is an error with the message, it is a JSON string but not a dictionary."

        print(f"ai_response : {ai_response}")

        # If we do a json dumps here it will be done again and re
        ai_response_formatted = json.dumps(ai_response)

    
        return self.create_new_message(profile, ai_response_formatted, type=response_type)

    def create_new_message(self, profile, message, type='user'):
        """
            @description: create new message
        """

        dbChatRoom = self.room.get('db')
        dbMessage = Message(
            chatroom=dbChatRoom,
            profile=profile,
            content=message,
            messageType=type
        )
        dbMessage.save()

        self.messages = load_last_100_message(dbChatRoom)
        return [
            dbMessage.serialize(FakeRequest()),
            # dbMessageReplyTest.serialize(FakeRequest()),
        ]

    def __str__(self) -> str:
        """
            @description: str
        """
        return 'aeuaoeu'