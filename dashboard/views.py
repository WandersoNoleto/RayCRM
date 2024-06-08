from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, Appointment, NextConsultDate
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
import json
from django.db.models.functions import Lower
from datetime import datetime

@login_required
def home(request):
    next_consult_date = NextConsultDate.objects.all().first()
    patients = Patient.objects.filter(clinic=request.user.clinic).order_by(Lower('name'))
    appointments = Appointment.objects.filter

    context = {
        'patients': patients,
        'next_consult_date': next_consult_date,
        'appointments': appointments
    }
    return render(request, 'index.html', context=context)

@login_required
def view_patients(request):
    patients = Patient.objects.filter(clinic=request.user.clinic).order_by(Lower('name'))
    context = {
        'patients': patients,
    }

    return render(request, 'patients.html', context=context)

@login_required
def add_patient(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            phone = data.get('phone')
            birth_date = data.get('birth_date')
            address = data.get('address')
            clinic = request.user.clinic

            print(name, phone, birth_date, address, clinic)

            patient = Patient(
                name=name,
                phone=phone, 
                birth_date=birth_date,
                address=address,
                clinic=clinic
            )

            patient.save()
            messages.success(request, 'Paciente adicionado com sucesso!')

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)})

    return redirect('view_patients')

@login_required
def get_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    data = {
        'id': patient.id,
        'name': patient.name,
        'phone': patient.phone,
        'birth_date': patient.birth_date,
        'address': patient.address,
    }
    return JsonResponse(data)


@login_required
def edit_patient(request, patient_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        patient = Patient.objects.get(id=patient_id)
        patient.name = data['name']
        print(patient.name)
        patient.phone = data['phone']
        patient.birth_date = data['birth_date']
        patient.address = data['address']
        patient.save()

        return JsonResponse({'status': 'success'})

@login_required 
def delete_patient(request, patient_id):
    print(patient_id)
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()

    return JsonResponse({'status': 'success'})

@login_required
def save_new_consult_date(request):
    if request.method == "POST":
        new_date = request.POST.get("nextConsultDate")

        NextConsultDate.objects.all().delete()
        next_date = NextConsultDate(date=new_date)
        next_date.save()

        return redirect('home')
    
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

        if Appointment.objects.filter(appointment_date=date, appointment_time=time_obj).exists():
            messages.error(request, "Não foi possível! Já existe um agendamento para esse horário, tente novamente")
            return redirect('home') 

        appointment = Appointment(patient=patient, appointment_date=date, appointment_time=time_obj)
        appointment.save()

        return redirect('home')
    
@login_required
def search_appointments(request):
    next_consult_date = NextConsultDate.objects.all().first()
    patients = Patient.objects.filter(clinic=request.user.clinic).order_by(Lower('name'))
    appointments = Appointment.objects.filter
    
    search_date = request.GET.get('search-date')
    search_name = request.GET.get('search-name')
    se_appointments = []

    if search_date or search_name:
        if search_date and search_name:
            se_appointments = Appointment.objects.filter(
                appointment_date=search_date,
                patient__name__icontains=search_name
            )
        elif search_date:
            se_appointments = Appointment.objects.filter(
                appointment_date=search_date
            )
        elif search_name:
            se_appointments = Appointment.objects.filter(
                patient__name__icontains=search_name
            )

    context = {
        'patients': patients,
        'next_consult_date': next_consult_date,
        'appointments': appointments,
        'se_appointments': se_appointments
    }

    return render(request, 'index.html', context=context)

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()

    return JsonResponse({'status': 'success'})