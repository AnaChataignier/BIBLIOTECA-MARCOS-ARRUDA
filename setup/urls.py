# projeto/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('biblioteca.urls')),  # Inclui as URLs do app biblioteca sob o prefixo /api/
]