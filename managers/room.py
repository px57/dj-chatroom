
from chatroom.managers.user import ChatUser
from chatroom.libs import load_last_100_message, serialize_messages_list
from chatroom.models import Message
from kernel.http.request import FakeRequest

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
        self.user_list.append(userinchat)
        self.users_count += 1

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
        for user in self.user_list:
            user.send_message(message)


    def receive(self):
        """
            @description: receive message
        """
        pass

    def create_new_message(self, profile, message):
        """
            @description: create new message
        """
        dbChatRoom = self.room.get('db')
        dbMessage = Message(
            chatroom=dbChatRoom,
            profile=profile,
            content=message,
        )
        dbMessage.save()

        dbMessageReplyTest = Message(
            chatroom=dbChatRoom,
            profile=profile,
            content='reply test',
            replyTo=dbMessage,
        )
        dbMessageReplyTest.save()

        self.messages = load_last_100_message(dbChatRoom)
        return [
            dbMessage.serialize(FakeRequest()),
            dbMessageReplyTest.serialize(FakeRequest()),
        ]

    def __str__(self) -> str:
        """
            @description: str
        """
        return 'aeuaoeu'