from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Appointment
from patients.models import Patient
from dashboard.models import NextConsultDate, PaymentMethods
from django.contrib import messages
from django.http import JsonResponse
from django.db.models.functions import Lower
from datetime import datetime

@login_required
def add_appointment(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        date = request.POST.get("date")
        hour = request.POST.get("hour")
        minute = request.POST.get("minute")

        patient = get_object_or_404(Patient, id=patient_id)

        time_str = f"{hour}:{minute}"
        time_obj = datetime.strptime(time_str, "%H:%M").time()

        if Appointment.objects.filter(date=date, time=time_obj).exists():
            messages.error(request, "Não foi possível! Já existe um agendamento para esse horário, tente novamente")
            return redirect('home') 

        appointment = Appointment(patient=patient, date=date, time=time_obj)
        appointment.save()

        return redirect('home')
    

@login_required
def search_appointments(request):
    search_date = request.GET.get('search-date')
    search_name = request.GET.get('search-name')
    se_appointments = []

    if search_date or search_name:
        if search_date and search_name:
            se_appointments = Appointment.objects.filter(
                date=search_date,
                patient__name__icontains=search_name
            )
        elif search_date:
            se_appointments = Appointment.objects.filter(
                date=search_date
            )
        elif search_name:
            se_appointments = Appointment.objects.filter(
                patient__name__icontains=search_name
            )

    appointments_data = []
    for appointment in se_appointments:
        appointments_data.append({
            'date': appointment.date.strftime('%d/%m/%Y'),
            'time': appointment.time.strftime('%H:%M'),
            'patient': appointment.patient.name,
            'id': appointment.id
        })

    request.session['se_appointments'] = appointments_data
    return redirect('home')

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()

    return JsonResponse({'status': 'success'})

@require_http_methods(["GET"]) 
def get_appointment_data(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        patient = appointment.patient
        payment_method_id = appointment.payment_method.id if appointment.payment_method else None

        data = {
            'id': appointment.id,
            'name': patient.name,
            'birth_date': patient.birth_date.strftime('%Y-%m-%d'),
            'phone': patient.phone,
            'payment_method': payment_method_id
        }
        return JsonResponse(data)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)

@require_http_methods(["POST"])
def save_appointment_payment_method(request):
    if request.method == "POST":
        payment_method_id = request.POST.get("payment-method")
        appointment_id = request.POST.get("appointment_id")

        appointment = get_object_or_404(Appointment, id=appointment_id)
        payment_method = get_object_or_404(PaymentMethods, id=payment_method_id)

        appointment.payment_method = payment_method
        appointment.save()

        return JsonResponse({'message': 'Método de pagamento do agendamento atualizado com sucesso.'}, status=200)

    return JsonResponse({'error': 'Método não permitido.'}, status=405)
