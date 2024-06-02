from django.contrib import admin
from .models import (
    Sales,
    Position,
    CSV
)

admin.site.register(Position)
admin.site.register(Sales)
admin.site.register(CSV)
