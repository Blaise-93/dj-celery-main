from django.urls import path
from .views import (
    home_view,
    SaleListView,
   # SalesDetailView, 
   sales_detail,
)

app_name = "sales"

urlpatterns = [
    path("", home_view, name="sales"),
    path("list/", SaleListView.as_view(), name="sales-list"),
    path("<int:pk>/", sales_detail, name="sales-detail"),
]
