from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/category/', include('categories.urls')),
    path('api/v1/', include('projects.urls')),
    path('api/v1/profile/', include('profiles.urls')),
]
