from django.db.models.signals import m2m_changed
from .models import Sales
from django.dispatch import receiver


@receiver(m2m_changed, sender=Sales.positions.through)
def calculate_total_price(sender, instance, action, **kwargs):
    print(instance)

    total_price = 0

    if action == "post_add" or action == "post_remove":
        for item in instance.get_positions():
            total_price += item.price
            print(total_price)

    instance.total_price = total_price
    instance.save()

