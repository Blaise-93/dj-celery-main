from django.test import TestCase
from .models import Post, Category
from profiles.models import UserProfile, User
from django.utils import timezone


class TestCreatePost(TestCase):

    @classmethod
    def setUpTestData(cls):

        test_category = Category.objects.create(name="category 1")

        testuser1 = User.objects.create(
            username="blaise", password="234wd"
        )

        user_profile, created = UserProfile.objects.get_or_create(
            user=testuser1)

        cls.post = Post.objects.create(
            category=test_category,
            title="Importance of Using Plasma TV",
            excerpt="excerpt",
            content="My content",
            slug="importance-of-using-plasma-tv",
            published="2024-05-07 20:48:14.596554+00:00",
            author=user_profile.user,
            status="status"
        )
# python manage.py test blogs.tests
    def test_blog_content(self):

        post = Post.objects.get(id=1)
        cat = Category.objects.get(id=1)
        author = f'{post.author}'
        excerpt = f'{post.excerpt}'
        title = f'{post.title}'
        content = f'{post.content}'
        status = f'{post.status}'
        slug = f'{post.slug}'
        published = f'{post.published}'

        self.assertEqual(author, 'blaise')
        self.assertEqual(title, 'Importance of Using Plasma TV')
        self.assertEqual(content, 'My content')
        self.assertEqual(excerpt, 'excerpt')
        self.assertEqual(status, 'status')
        self.assertEqual(str(post), 'Importance of Using Plasma TV')
        self.assertEqual(str(cat), 'category 1')
        self.assertEqual(published, "2024-05-07 20:48:14.596554+00:00")
        self.assertEqual(slug, 'importance-of-using-plasma-tv')
