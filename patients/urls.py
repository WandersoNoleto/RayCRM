
from django.urls import path
from .  import views
import dashboard.views as dash_views

urlpatterns = [
    path('', dash_views.view_patients, name="view_patients"),
    path('add/', views.add_patient, name="add_patient"),
    path('edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('get/<int:patient_id>/', views.get_patient, name='get_patient'),
]
