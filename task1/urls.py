from django.urls import path
from .views import review

app_name = 'task1'

urlpatterns = [
    path('', review, name='review')
]
