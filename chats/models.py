from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=12)
    first_name = models.CharField(max_length=12)
    las_name = models.CharField(max_length=12)
    author = models.CharField(max_length=12)

    def __str__(self) -> str:
        return self.title
