
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),

    path('', include('dashboard.urls')),
    path('appointments/', include('appointments.urls')),
    path('patients/', include('patients.urls')),    
]
