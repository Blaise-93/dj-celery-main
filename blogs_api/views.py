from rest_framework import generics
from blogs.models import Post
from .serializers import PostSerializer, RegisteredUserSerializer
from rest_framework.permissions import (
    BasePermission, IsAdminUser,
    IsAuthenticated, AllowAny,
    DjangoModelPermissionsOrAnonReadOnly,
    SAFE_METHODS
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PostUserWritePermission(BasePermission):

    message = 'Editing posts is restricted to the author only'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:  # GET, POST etc

            return True
        return obj.author == user  # filter


class CustomUserCreate(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        registered_user_serializer = RegisteredUserSerializer(
            data=request.data)
        if registered_user_serializer.is_valid():
            newuser = registered_user_serializer.save()

            if newuser:
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PostList(generics.ListCreateAPIView):
    """ can post and list individual posts"""

    serializer_class = PostSerializer
   # permission_classes = [IsAuthenticated ]

    def get_queryset(self):
        author = self.request.user
        queryset = Post.objects.all()  # filter(author=author.id)
        return queryset


""" 
Permission Levels - DRF
    Project level
    view level
    object level
"""


class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    """ can get individual post"""
    # queryset = Post.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly,]
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
