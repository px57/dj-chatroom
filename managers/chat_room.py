from channels.generic.websocket import WebsocketConsumer
from chatroom.models import ChatRoom, Message
from profiles.models import Profile
from chatroom.managers.room import RoomManager
from chatroom.managers.user import ChatUser
from datetime import datetime

class ChatRoomManager:
    """
        @description: ChatRoomManager class 
        @example: Liste des rooms, avec les utilisateurs connectés.
        room_list = {
            '$room_name': {
                "db": <ChatRoom: ChatRoom object (1)>,
                "last_use": "2021-05-01 12:00:00",
                "roomManager": RoomManager(),
            }
        }
    """

    def __init__(self) -> None:
        self.room_list = {}

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ [CREATE]

    def create_new_dbRoom(self, room_name: str) -> ChatRoom:
        """
            @description: create new room
        """
        dbChatRoom = ChatRoom.objects.create(name=room_name)
        dbChatRoom.save()
        return dbChatRoom

    def __create_room__incache(self, dbChatRoom: ChatRoom) -> None:
        """
            @description: create room in cache
        """
        if self.__find_dbRoom_by_name__incache(dbChatRoom.name) is not None:
            return None
        
        self.room_list[dbChatRoom.name] = {
            "db": dbChatRoom,
        }
        self.room_list[dbChatRoom.name].update({
            "last_use": datetime.now(),  
            "roomManager": RoomManager(self.room_list[dbChatRoom.name]),
        })
        return None

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ [FIND]
    def __find_dbRoom_by_name__incache(self, room_name: str) -> ChatRoom:
        """
            @description: find room by name in cache
        """
        # -> ChatRoom
        if room_name in self.room_list:
            return self.room_list[room_name]["db"]
        return None
    
    def find_dbRoom_by_name(self, room_name: str) -> ChatRoom:
        """
            @description: find room by name
        """
        dbChatRoom = self.__find_dbRoom_by_name__incache(room_name)
        if dbChatRoom is not None:
            return dbChatRoom
        
        dbChatRoom = ChatRoom.objects.filter(name=room_name).first()
        return dbChatRoom
    
    def find_or_create_dbRoom(self, room_name: str) -> ChatRoom:
        """
            @description: 
        """
        dbChatRoom = self.find_dbRoom_by_name(room_name)
        if dbChatRoom is None:
            dbChatRoom = self.create_new_dbRoom(room_name)

        self.__create_room__incache(dbChatRoom)
        return dbChatRoom
    
    def find_room_by_name(self, room_name: str) -> dict:
        """
            @description: find room by name
        """
        if room_name in self.room_list:
            return self.room_list[room_name]
        return None
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ [CONNECT]
    def connect(self, room_name: str, consumer: WebsocketConsumer) -> None:
        """
            @description: connect user to room
        """
        self.find_or_create_dbRoom(room_name)
        room = self.find_room_by_name(room_name)
        return room["roomManager"].connect(consumer)


CHATROOM_MANAGER = ChatRoomManager()