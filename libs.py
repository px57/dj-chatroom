from chatroom.models import ChatRoom, Message
from kernel.http.request import FakeRequest


def load_last_100_message(dbChatRoom=None):
    return load_last_n_message( 100, dbChatRoom)

def load_last_n_message( n_message: int, dbChatRoom=None):
    """
        @description: 
    """
    messages = Message.objects.filter(
        chatroom=dbChatRoom
    )[0:n_message]
    print ('messages', messages)
    return messages

def serialize_messages_list(messages):
    """
        @description: 
    """
    serialized = []
    for message in messages:
        serialized.append(message.serialize(FakeRequest()))
    serialized = list(reversed(serialized))
    return serialized
