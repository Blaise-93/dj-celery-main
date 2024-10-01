from django.contrib import admin
from .models import (
    Product,
    Stock,
    StockMovement,
    Order,
    Supplier,
    Refund
)


admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(StockMovement)
admin.site.register(Order)
admin.site.register(Supplier)
admin.site.register(Refund)
