from django.urls import path
from .views import PostList, PostDetail, UpdatePost, DeletePost

app_name = "blogs_api"


urlpatterns = [
    path("", PostList.as_view(), name="listcreate"),
    path("<int:pk>/", PostDetail.as_view(), name="blog-detail"),
    path("<int:pk>/update/", UpdatePost.as_view(), name="blog-update"),
    path("<int:pk>/delete/", DeletePost.as_view(), name="blog-delete"),
   
]
