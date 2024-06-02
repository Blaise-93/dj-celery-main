from django.urls import path
from .views import PostList, PostDetail

app_name = "blogs_api"


urlpatterns = [
    path("", PostList.as_view(), name="listcreate"),
    path("<int:pk>/", PostDetail.as_view(), name="blog-detail"),
   
]
