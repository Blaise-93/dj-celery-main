from django.urls import path
from .views import project_stats

app_name = "reports"

urlpatterns = [
    path("", project_stats, name="project")
]
