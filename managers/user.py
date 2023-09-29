import json

class ChatUser:
    """
        @description: ChatUser class
    """

    def __init__(self, consumer, room):
        """
            @description: constructor
        """
        self.consumer = consumer
        self.scope = consumer.scope
        self.room = room

        if consumer.scope['user'].is_anonymous:
            return;

        self.user = self.scope['user']
        self.profile = self.scope['profile']


    def send_message(self, message: dict) -> None:
        """
            @description: 
        """
        json_message = json.dumps(message)
        self.consumer.send(text_data=json_message)