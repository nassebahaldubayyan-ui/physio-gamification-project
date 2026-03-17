from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # API URLs
    path('', include('web_.urls')),  # Main URLs for your app
]