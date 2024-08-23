from django.urls import path
from .views import(
project_stats, generate_report_view,
 ReportCreateView,
 load_products, products
) 

# generate_report

app_name = "reports"

urlpatterns = [
    path("", project_stats, name="project"),
    path("save-report/", ReportCreateView.as_view(), name='generate-report'),
    path("product/", products, name='product'),
    path("load-products/", load_products, name='load-products')
    #path("save-report/", generate_report_view, name='generate-report')
]
