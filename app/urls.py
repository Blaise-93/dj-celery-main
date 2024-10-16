from django.urls import path
from django.contrib import admin
from .views import home

app_name='app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage/', home, name="home")
]
