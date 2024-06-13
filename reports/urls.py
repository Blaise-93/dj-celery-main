from django.urls import path
from .views import project_stats, generate_report_view, ReportCreateView
# generate_report

app_name = "reports"

urlpatterns = [
    path("", project_stats, name="project"),
    path("save-report/", ReportCreateView.as_view(), name='generate-report')
    #path("save-report/", generate_report_view, name='generate-report')
]
