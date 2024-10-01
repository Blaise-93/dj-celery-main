from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Product,
    Stock,
    StockMovement,
    Supplier,
    Order,
    Refund
)


class ProductListView(LoginRequiredMixin, generic.ListView):
    queryset = Product.objects.all().distinct()
    context_object_name = 'products'
    template_name = 'inventory/products/product-list.html'
    ordering = '-date_created'
