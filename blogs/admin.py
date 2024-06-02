from django.contrib import admin

from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = [

        "category",
        "title",
        "id",
        "status",
        "slug",
        "author",
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(Category)