from rest_framework import generics
from blogs.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated



class PostList(generics.ListCreateAPIView):
    """ can post and list individual posts"""

    serializer_class = PostSerializer
    permission_classes = [IsAdminUser, ]

    def get_queryset(self):
        author = self.request.user
        queryset = Post.objects.all() #filter(author=author.id)
        return queryset

""" 
Permission Levels - DRF
    Project level
    view level
    object level
"""

class PostDetail(generics.RetrieveAPIView):
    """ can get individual post"""
    # queryset = Post.objects.all()

    # return all the queryset flagged as published
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UpdatePost(generics.UpdateAPIView):

    """ can edit the post of the user from our db """

    queryset = Post.objects.all().distinct()
    serializer_class = PostSerializer


class DeletePost(generics.DestroyAPIView):

    """ delete a post made by the user """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
