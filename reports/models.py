from django.db import models
from django.utils import timezone
# Create your models here.


class Report(models.Model):

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="reports", blank=True)
    remarks = models.TextField()
    author = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    responsible = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE)
    week_number = models.CharField(max_length=2, blank=True)
    end_date = models.DateField()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.week_number == "":
            self.week_number = self.start_date.isocalendar()[1]
            self.start_date = timezone.datetime.date()
        super().save(*args, **kwargs)
