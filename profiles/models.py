from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

class User(AbstractUser):
    pass

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(default="no bio..")
    avatar = models.ImageField(upload_to="avatar", default="no_picture.png")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Profile of {self.user.username.title()}'
    
    


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username
    
    


def post_user_created_signal(sender, instance, created, **kwargs):
    """ listing the admin events """

    user = instance
    print(sender)
    print(created)
    print(user)
    try:
        if created:
            UserProfile.objects.create(user=user)
    except ObjectDoesNotExist:
        UserProfile.objects.create(user=user)

post_save.connect(post_user_created_signal, sender=User)