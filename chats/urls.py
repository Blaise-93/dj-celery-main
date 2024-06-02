from django.urls import path
from chats.views import chat_room

app_name = "chats"

url_patterns = [
            path('', chat_room, name="chat-list"),
]