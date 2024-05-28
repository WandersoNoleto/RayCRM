from django.urls import path, include
from .  import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('login-check/', views.login_check, name="login_check"),
    path('register/', views.register_view, name="register"), 
    path('user-storage/', views.user_storage, name="user_storage")
]
