from django.urls import path
from . import views

urlpatterns = [  
    path('add', views.add_appointment, name="add_appointment"),
    path('search', views.search_appointments, name='search_appointments'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('get/<int:appointment_id>/', views.get_appointment_data, name='get_appointment_data'),
    path('edit-pay-method/', views.save_appointment_payment_method, name='save_appointment_payment_method'),
    path('missed/<int:appointment_id>/', views.set_missed_appointment, name="set_missed_appointment")
]
