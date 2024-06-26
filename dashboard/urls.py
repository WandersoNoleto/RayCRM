from django.urls import path
from .  import views

urlpatterns = [
    path('', views.home, name="home"),
    path('next-consult-date/save', views.save_new_consult_date, name='save_next_consult_date'),
    path('get-next-consult-date/', views.get_next_consult_date, name='get_next_consult_date'),
    
    path('start-queue/', views.start_queue, name='start_queue'),
    path('update-queue-stats/<int:appointment_id>/', views.update_queue_stats, name='update_queue_stats'),
    path('check-queue-state/', views.check_queue_state, name='check_queue_status'),
    path('finalize-queue/', views.finalize_queue, name='finalize_queue'),
    path('finalize-queue-confirm/', views.finalize_queue_confirm, name='finalize_queue_confirm'),

    path('settings/', views.settings_view, name="settings"),
    path('payment-methods/add', views.add_payment_method, name="add_payment_method"),
    path('payment-methods/delete/<int:id>/', views.delete_payment_method, name="delete_payment_method"),


    path('doctor-view/',views.home_doctor, name="doctor_view")
]
