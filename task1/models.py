from django.db import models

# Create your models here.

class Review(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    review = models.TextField()
    dete_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name


