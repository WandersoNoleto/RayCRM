from django.urls import path, include
from .  import views

urlpatterns = [
    path('', views.home, name="home"),
    path('pacients/', views.view_pacients, name="view_pacients")
]
