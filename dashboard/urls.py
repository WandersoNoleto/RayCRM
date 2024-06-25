from django.urls import path
from .  import views

urlpatterns = [
    path('', views.home, name="home"),
    path('next-consult-date/save', views.save_new_consult_date, name='save_next_consult_date'),
    
    path('appointment/add', views.add_appointment, name="add_appointment"),
    path('appointments/search', views.search_appointments, name='search_appointments'),
    path('appointments/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('appointments/get/<int:appointment_id>/', views.get_patient_data, name='get_patient_data'),

    path('patients/', views.view_patients, name="view_patients"),
    path('patients/add/', views.add_patient, name="add_patient"),
    path('patients/edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('patients/get/<int:patient_id>/', views.get_patient, name='get_patient'),

    path('settings/', views.settings_view, name="settings"),
    path('payment-methods/add', views.add_payment_method, name="add_payment_method")
]
