from django.contrib import admin
from .models import (
    Product,
    Stock,
    StockMovement,
    PurchaseOrder,
    Supplier,
    Refund,
    OrderItem
)


admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(StockMovement)
admin.site.register(PurchaseOrder)
admin.site.register(Supplier)
admin.site.register(OrderItem)
admin.site.register(Refund)
