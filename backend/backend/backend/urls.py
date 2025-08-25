from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("backend_app.urls")), 
     path('', lambda request: redirect('api/monitor/')),
]
