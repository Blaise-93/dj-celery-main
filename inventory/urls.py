from django.urls import path
from .views import (
    ProductListView
)


app_name = "inventory"

urlpatterns = [
    path('', ProductListView.as_view(), name='product'),
]
