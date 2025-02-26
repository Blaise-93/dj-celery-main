from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('blogs/', include('blogs.urls', namespace='blogs')),
    path('chatroom/', include('chatrooms.urls', namespace='chatrooms')),
    path('', include('task1.urls', namespace='task1')),

    path('products/', include('products.urls', namespace='products')),
    path('customers/', include('customers.urls', namespace='customers')),
    path('sales/', include('sales.urls', namespace='sales')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('inventory/', include('inventory.urls', namespace='inventory')),
    path('app/', include('app.urls', namespace='app')),

    # API
    path('api/', include('blogs_api.urls', namespace='blogs_api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('chats/', include('chats.urls', namespace='chats')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    urlpatterns += path("__reload__/", include("django_browser_reload.urls")),
