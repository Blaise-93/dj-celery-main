from django.urls import path
from .views import chat_room, home_page

app_name = "chatrooms"

urlpatterns = [
    path("",  home_page, name='chatroom'),
    path("<str:room_name>/",  chat_room, name='room'),
]
