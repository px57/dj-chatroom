from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = [
        
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        
    ]