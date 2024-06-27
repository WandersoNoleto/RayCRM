from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import NextConsultDate, PaymentMethods
from appointments.models import Appointment
from patients.models import Patient
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import QueueState
from datetime import datetime, timedelta, date

@login_required
def home(request):
    queue_state = request.session.get('queue_state', {'is_started': False})
    next_consult_date = NextConsultDate.objects.all().first()
    patients = Patient.objects.filter(clinic=request.user.clinic).order_by(Lower('name'))
    appointments = Appointment.objects.filter(date=next_consult_date.date)
    payment_methods = PaymentMethods.objects.all()
    today_date = date.today()
    se_appointments = request.session.pop('se_appointments', [])

    context = {
        'patients': patients,
        'queue_state': queue_state,
        'next_consult_date': next_consult_date,
        'appointments': appointments,
        'payment_methods': payment_methods,
        'today_date': today_date,
        'se_appointments': se_appointments,
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
def save_new_consult_date(request):
    if request.method == "POST":
        new_date = request.POST.get("nextConsultDate")
        current_date = NextConsultDate.objects.all().first().date

        appointments = Appointment.objects.filter(date=current_date)
        for appointment in appointments:
            appointment.date = new_date
            appointment.save()

        NextConsultDate.objects.all().delete()
        next_date = NextConsultDate(date=new_date)
        next_date.save()

        return redirect('home')

@login_required
def get_next_consult_date(request):
    next_consult_date = NextConsultDate.objects.first()
    if next_consult_date:
        return JsonResponse({'next_consult_date': next_consult_date.date.strftime('%Y-%m-%d')})
    else:
        return JsonResponse({'next_consult_date': None})
    

@login_required
def settings_view(request):
    payment_methods = PaymentMethods.objects.all()

    context={
        'payment_methods': payment_methods
    }

    return render(request, 'settings.html', context)


def add_payment_method(request):
    if request.method == "POST":
        name = request.POST.get("payment_method")

        payment_method = PaymentMethods(name=name)
        payment_method.save()

        return redirect('settings')

        
def delete_payment_method(request, id):
    payment_method = get_object_or_404(PaymentMethods, id=id)

    payment_method.delete()

    return redirect('settings')


@require_GET
def start_queue(request):
    try:
        queue_state, created = QueueState.objects.get_or_create()
        queue_state.is_started = True

        queue_state.save()

        return JsonResponse({'success': 'Fila iniciada com sucesso'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def update_last_treated_appointment(request, appointment_id):
    print(f'Update_last_treated_appointment.......................{appointment_id}')
    try:
        queue_state, created = QueueState.objects.get_or_create()
        appointment = Appointment.objects.get(id=appointment_id)

        queue_state.is_started = True
        queue_state.last_treated_appointment = appointment

        queue_state.save()

        return JsonResponse({'success': f'Último agendamento tratado atualizado para {appointment_id}'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def check_queue_state(request):
    try:
        queue_state, created = QueueState.objects.get_or_create()
        return JsonResponse({
            'is_started': queue_state.is_started,
            'last_treated_appointment': {
                'id': queue_state.last_treated_appointment.id,
                'patient_name': queue_state.last_treated_appointment.patient.name if queue_state.last_treated_appointment else None
            } if queue_state.last_treated_appointment else None
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def finalize_queue(request):
    try:
        queue_date = NextConsultDate.objects.all().first().date
        total_patients = Appointment.objects.filter(date=queue_date).count()

        payment_method_counts = {}
        appointments = Appointment.objects.filter(date=queue_date)
        for appointment in appointments:
            method = appointment.payment_method
            if method:
                if method.name in payment_method_counts:
                    payment_method_counts[method.name] += 1
                else:
                    payment_method_counts[method.name] = 1
        
        return JsonResponse({
            'total_patients': total_patients,
            'payment_method_counts': payment_method_counts,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def finalize_queue_confirm(request):
    today = datetime.today().date()


    next_consult_date_obj = NextConsultDate.objects.first()
    next_consult_date = next_consult_date_obj.date


    appointments = Appointment.objects.filter(date=next_consult_date)
    for appointment in appointments:
        patient = appointment.patient
        patient.last_appointment = next_consult_date
        patient.save()

    appointments.delete()

    next_consult_date += timedelta(days=(2 - next_consult_date.weekday()) % 7)
    if next_consult_date <= today:
        next_consult_date += timedelta(days=7)

    while next_consult_date.weekday() != 2:
        next_consult_date += timedelta(days=1)

    next_consult_date_obj.date = next_consult_date
    next_consult_date_obj.save()

    queue_state = QueueState.objects.all().first()
    queue_state.is_started = False
    queue_state.last_treated_appointment_id = None
    queue_state.save()

    return redirect('home')