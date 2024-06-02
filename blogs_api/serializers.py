from blogs.models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = [
            'category',
            "id", 
            "title",
            "author",
            "excerpt",
            "content",
            "status"
        ]
