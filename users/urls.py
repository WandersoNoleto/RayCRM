from django.urls import path, include
from .  import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('login-check/', views.login_check, name="login_check"),

    path('register/choices/', views.register_choices_view, name="register_choices_view"),

    path('register-doctor-view/', views.register_doctor_view, name="register_doctor_view"), 
    path('register-doctor/', views.register_doctor, name="register_doctor"), 
    path('register-receptionist-view/', views.register_receptionist_view, name="register_receptionist_view"), 
    path('register-receptionist/', views.register_receptionist, name="register_receptionist"), 

    path('logout/', views.logout_view,name="logout"),
]
