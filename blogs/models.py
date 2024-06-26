from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categories"
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):

    class PostObjects(models.Manager):

        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    OPTIONS = (
        ("draft", "Draft"),
        ('published', 'Published')
    )

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1
    )

    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    content = models.TextField()
    slug = models.SlugField(max_length=200, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey("profiles.User", on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=OPTIONS, default='published')

    objects = models.Manager() # default manager
    postobject = PostObjects() # custom manager

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):

        self.slug = slugify(self.title[:31])

        return super().save(*args, **kwargs)
    
