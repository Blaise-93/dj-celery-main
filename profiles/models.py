from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
# from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", 'Student'
        TEACHER = 'Teacher', "Teacher"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class StudentManager(BaseUserManager):
    """ query and filter out the student role in
        the db """

    def get_queryset(self, *args, **kwargs):

        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):

    base_role = User.Role.STUDENT

    student = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):

        return "Only for students"


class TeacherManager(BaseUserManager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)\
            .filter(role=User.Role.TEACHER)


class Teacher(User):

    base_role = User.Role.TEACHER

    teacher = TeacherManager()
    """ Teacher.teacher.all()
        <QuerySet [<Teacher: Ngozi>]> 
        pip install black or

        python3 -m black
        """
    class Meta:
        proxy = True

    def welcome(self):

        return "Only for teachers"


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


class StudentProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)


def create_user_profile_for_student(sender, instance, created, **kwargs):

    user = instance
    try:
        if created and user.role == "STUDENT":
            StudentProfile.objects.create(user=user)
    except ObjectDoesNotExist:
        pass

class TeacherProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)


def create_user_profile_for_teacher(sender, instance, created, **kwargs):

    user = instance
    print(sender)
    try:
        if created and user.role == "TEACHER":
            StudentProfile.objects.create(user=user)
    except ObjectDoesNotExist:
        pass

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
        pass

post_save.connect(create_user_profile_for_student, sender=Student)
post_save.connect(post_user_created_signal, sender=User)
post_save.connect(create_user_profile_for_teacher, sender=Teacher)