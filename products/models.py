from django.db import models


class Product(models.Model):

    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch_Dinner', 'Lunch & Dinner'),
        ('Beverages_Drinks', 'Beverages & Drinks'),
    ]

    SUBCATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('beverages_and_drink', 'Beverages and Drinks'),
        ('rice', 'Rice Meal'),
        ('beef_in_stew_sauce', 'Beef In Stew/Sauce'),
        ('chicken_in_stew_and_sauce', 'Chicken In Stew/Sauce'),
        ('protein', 'Protein'),
        ('soups', 'Soups'),
        ('native_pot', 'Native Pot'),
        ('pasta_and_noodles', 'Pasta/Noodles'),
        ('seafood_in_stew_sauce', 'Seafood In Stew/Sauce'),
        ('swallow', 'Swallow'),
        ('sides', 'Sides'),
        ('platter', 'Platter'),
        ('salad', 'Salad'),

    ]

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products', default='no_picture.png')
    price = models.FloatField(
        help_text="in US dollars ($)", verbose_name="price")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=30, choices=SUBCATEGORY_CHOICES)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        stringified_date = self.date_created.strftime("%d/%m/%Y")

        return f'{self.name} — {stringified_date}'

    class Meta:
        ordering = ['-date_created']
