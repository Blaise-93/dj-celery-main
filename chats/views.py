from django.shortcuts import render
from .models import Post
from .forms import PostForm

# Create your views here.

def chat_room(request):
    context = {
        "first_name": "Blaise",
        "age":30,
        'school': "UNN"
    }
    return render(request, "chats/chats_list.html", context)


def post_list(request):

    post = Post.objects.all()
    context = {
        "post": post
    }

    return render(request, "chats/chats_list.html", context)

def post_create(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm()
    if request == "POST":
        form = PostForm(request.POST or None)
        if form.is_valid():
            form.save()
    



