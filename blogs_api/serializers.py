from blogs.models import Post
from rest_framework import serializers
from profiles.models import User


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


class RegisteredUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', "last_name"]
        extra_kwargs = {'password': {"write_only": True}}

    def create(self, validated_data):
        # return super().create(validated_data)
        password = validated_data.pop("password", None)
        user = self.Meta.model(**validated_data)

        if password is not None:
            user.set_password(password)
            user.save()

            return user
