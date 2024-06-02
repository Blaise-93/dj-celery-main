from rest_framework import generics
from blogs.models import Post
from .serializers import PostSerializer

class PostList(generics.ListCreateAPIView):
    """ can post individual post, and list each view """

    queryset = Post.objects.all()
    serializer_class = PostSerializer



class PostDetail(generics.RetrieveDestroyAPIView):
    """ can get individual post, and delete each view """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
