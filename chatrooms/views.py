from django.shortcuts import render

# Create your views here.

def home_page(request):

    return render(request, "chatrooms/homepage.html")

def chat_room(request, room_name):
    context = {
        "first_name": "Blaise",
        "age":30,
        'school': "UNN",
        'room_name': room_name
    }
    return render(request, "chatrooms/chatroom.html", context)