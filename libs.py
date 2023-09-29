from chatroom.models import ChatRoom, Message
from kernel.http.request import FakeRequest


def load_last_100_message(chat_room=None):
    """
        @description: 
    """
    if chat_room is None:
        return Message.objects.all()[0: 100]
    
    messages = Message.objects.filter(
        chatroom=chat_room
    ).order_by('-created_at')[:100]
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
