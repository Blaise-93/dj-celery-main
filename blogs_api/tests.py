from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blogs.models import Post, Category
from profiles.models import User, UserProfile


class PostsTests(APITestCase):

    def test_view_posts(self):

        url = reverse("blogs_api:listcreate")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        
        self.test_category = Category.objects.create(name= "category 1")

        self.test_user = User.objects.create(username="blaise", password="password")
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.test_user)

        data = {
            "title": "new",
            "author": 1,
            'excerpt': "excerpt",
            "content":"content"
        }

        url = reverse("blogs_api:listcreate")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

