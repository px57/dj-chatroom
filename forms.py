
from chatroom.models import ChatRoom, Message
from django import forms

class NewChatRoomForms(forms.Form):
    """
       @decription: 
    """
    name = forms.CharField(max_length=100)
    
    def clean_name(self):
        """
            @description: 
        """
        name = self.cleaned_data.get('name')
        if ChatRoom.objects.filter(name=name).exists():
            raise forms.ValidationError("Room name already exists")
        return name