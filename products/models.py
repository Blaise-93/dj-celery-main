from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products', default='no_picture.png')
    price = models.FloatField(help_text="in US dollars ($)", verbose_name="price")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        stringified_date = self.date_created.strftime("%d/%m/%Y")
    
        return f'{self.name} — {stringified_date}'
    
