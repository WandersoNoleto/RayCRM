from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import NextConsultDate, PaymentMethods
from appointments.models import Appointment
from patients.models import Patient
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import QueueState

@login_required
def home(request):
    queue_state = request.session.get('queue_state', {'is_started': False})
    next_consult_date = NextConsultDate.objects.all().first()
    patients = Patient.objects.filter(clinic=request.user.clinic).order_by(Lower('name'))
    appointments = Appointment.objects.filter
    payment_methods = PaymentMethods.objects.all()

    context = {
        'patients': patients,
        'queue_state': queue_state,
        'next_consult_date': next_consult_date,
        'appointments': appointments,
        'payment_methods': payment_methods
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

        NextConsultDate.objects.all().delete()
        next_date = NextConsultDate(date=new_date)
        next_date.save()

        return redirect('home')
    

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
    try:
        queue_state, created = QueueState.objects.get_or_create()
        appointment = Appointment.objects.get(id=appointment_id)
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

