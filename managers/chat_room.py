from channels.generic.websocket import WebsocketConsumer
from chatroom.models import ChatRoom
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



    def __create_room__incache(self, dbChatRoom: ChatRoom) -> None:
        """
            @description: create room in cache
        """
        if self.__find_dbRoom_by_name__incache(dbChatRoom.id) is not None:
            return None
        
        self.room_list[dbChatRoom.id] = {
            "db": dbChatRoom,
        }
        self.room_list[dbChatRoom.id].update({
            "last_use": datetime.now(),  
            "roomManager": RoomManager(self.room_list[dbChatRoom.id]),
        })
        return None

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ [FIND]
    def __find_dbRoom_by_name__incache(self, room_id: int) -> ChatRoom:
        """
            @description: find room by name in cache
        """
        # -> ChatRoom
        if room_id in self.room_list:
            return self.room_list[room_id]["db"]
        return None
    
    def find_dbRoom_by_name(self, room_id: int) -> ChatRoom:
        """
            @description: find room by name
        """
        dbChatRoom = self.__find_dbRoom_by_name__incache(room_id)
        if dbChatRoom is not None:
            return dbChatRoom
        
        dbChatRoom = ChatRoom.objects.filter(name=room_id).first()
        return dbChatRoom
    
    def find_or_create_dbRoom(self, dbChatRoom: ChatRoom) -> ChatRoom:
        """
            @description: 
        """
        self.__create_room__incache(dbChatRoom)
        return dbChatRoom
    
    def find_room_by_id(
            self: object, 
            room_id: int
        ) -> dict or None: 
        """
            @description: 
        """
        if room_id in self.room_list:
            return self.room_list[room_id]
        return None
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ [CONNECT]
    def connect(
        self: object, 
        dbChatRoom: ChatRoom, 
        consumer: WebsocketConsumer
    ) -> None:
        """
            @description: connect user to room
            @params.dbChatRoom: The room to connect.
            @params.consumer: The consumer to connect.

        """
        self.find_or_create_dbRoom(dbChatRoom)
        room = self.find_room_by_id(dbChatRoom.id)

        print( f"room :{room}" )
        return room["roomManager"].connect(consumer)


CHATROOM_MANAGER = ChatRoomManager()