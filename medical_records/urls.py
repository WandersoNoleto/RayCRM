from . import views
from django.urls import path

urlpatterns = [
    path('create-pdf/', views.create_pdf, name='create_pdf'),
]
