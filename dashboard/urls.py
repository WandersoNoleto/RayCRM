from django.urls import path, include
from .  import views

urlpatterns = [
    path('', views.home, name="home"),
    path('patients/', views.view_patients, name="view_patients"),
    path('patients/add/', views.add_patient, name="add_patient"),
    path('patients/edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('patients/get/<int:patient_id>/', views.get_patient, name='get_patient'),
]
