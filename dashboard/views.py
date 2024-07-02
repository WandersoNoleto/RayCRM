from django.shortcuts import render, redirect, get_object_or_404
from .models import NextConsultDate, PaymentMethods
from appointments.models import Appointment, ConsultationDaySummary
from patients.models import Patient
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import QueueState
from datetime import datetime, timedelta, date
from users.decorators import user_is_clinic, user_is_doctor, user_is_partner_optic, user_is_receptionist
from medical_records.models import MedicalRecord

@user_is_receptionist
def home(request):
    queue_state = request.session.get('queue_state', {'is_started': False})
    next_consult_date = NextConsultDate.objects.all().first()
    patients = Patient.objects.filter(clinic=request.user.receptionist.clinic).order_by(Lower('name'))
    appointments = Appointment.objects.filter(date=next_consult_date.date)
    appointments_type_c =  Appointment.objects.filter(date=next_consult_date.date).filter(type="Consulta").count()
    appointments_type_r =  Appointment.objects.filter(date=next_consult_date.date).filter(type="Retorno").count()
    payment_methods = PaymentMethods.objects.all()
    today_date = date.today()
    se_appointments = request.session.pop('se_appointments', [])
    consultation_day_summaries = ConsultationDaySummary.objects.all()
    queue_state_stats = QueueState.objects.all().first()

    context = {
        'patients': patients,
        'queue_state': queue_state,
        'queue_state_stats': queue_state_stats,
        'next_consult_date': next_consult_date,
        'appointments': appointments,
        'appointments_type_c': appointments_type_c,
        'appointments_type_r': appointments_type_r,
        'payment_methods': payment_methods,
        'today_date': today_date,
        'se_appointments': se_appointments,
        'consultation_day_summaries': consultation_day_summaries
    }
    return render(request, 'receptionist/index.html', context=context)


@user_is_receptionist
def view_patients(request):
    patients = Patient.objects.filter(clinic=request.user.receptionist.clinic).order_by(Lower('name'))
    context = {
        'patients': patients,
    }

    return render(request, 'receptionist/patients.html', context=context)

@user_is_receptionist
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

@user_is_receptionist
def get_next_consult_date(request):
    next_consult_date = NextConsultDate.objects.first()
    print(next_consult_date)
    if next_consult_date:
        return JsonResponse({'next_consult_date': next_consult_date.date.strftime('%Y-%m-%d')})
    else:
        return JsonResponse({'next_consult_date': None})
    

@user_is_receptionist
def settings_view(request):
    payment_methods = PaymentMethods.objects.all()

    context={
        'payment_methods': payment_methods
    }

    return render(request, 'receptionist/settings.html', context)


@user_is_receptionist
def add_payment_method(request):
    if request.method == "POST":
        name = request.POST.get("payment_method")

        payment_method = PaymentMethods(name=name)
        payment_method.save()

        return redirect('settings')

@user_is_receptionist       
def delete_payment_method(request, id):
    payment_method = get_object_or_404(PaymentMethods, id=id)

    payment_method.delete()

    return redirect('settings')

@user_is_receptionist
@require_GET
def start_queue(request):
    try:
        queue_state, created = QueueState.objects.get_or_create()
        queue_state.is_started = True

        queue_state.save()

        return JsonResponse({'success': 'Fila iniciada com sucesso'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@user_is_receptionist
@require_GET
def update_queue_stats(request, appointment_id):
    try:
        queue_state, created = QueueState.objects.get_or_create()
        appointment = Appointment.objects.get(id=appointment_id)
        date_today = date.today()
        appointment.status = 'attended'
        appointment.save()

        queue_state.is_started = True
        queue_state.last_treated_appointment = appointment

        queue_state.total = Appointment.objects.filter(date=date_today).count()
        queue_state.consultations = Appointment.objects.filter(type='Consulta').filter(date=date_today).count()
        queue_state.follow_ups = Appointment.objects.filter(type='Retorno').filter(date=date_today).count()
        queue_state.attendeds = Appointment.objects.filter(status='attended').filter(date=date_today).count()
        queue_state.waiting = Appointment.objects.filter(status='waiting').filter(date=date_today).count()
        queue_state.misseds = Appointment.objects.filter(status='missed').filter(date=date_today).count()

        queue_state.save()

        return JsonResponse({'success': f'Último agendamento tratado atualizado para {appointment_id}'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@user_is_receptionist
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


@user_is_receptionist
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


@user_is_receptionist
def add_consultation_day_summary(request):
    print("in consult")
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
        
        consultation_day_summary = ConsultationDaySummary(
            consultation_date = queue_date,
            total_patients = total_patients,
            payment_method_counts = payment_method_counts
        )

        print("aaa")

        consultation_day_summary.save()
        print(f"{consultation_day_summary.date} - {consultation_day_summary.total_patients} - {consultation_day_summary.payment_method_counts}")

        return redirect("home")
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@user_is_receptionist
def finalize_queue_confirm(request):
    add_consultation_day_summary(request)

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


@user_is_doctor
def home_doctor(request):
    queue_state = QueueState.objects.all().first()
    context = {}

    if queue_state.is_started == True:
        current_patient_id = queue_state.last_treated_appointment.patient.id
        current_patient = Patient.objects.filter(id=current_patient_id).first()

        medical_records = MedicalRecord.objects.filter(id=current_patient.id)

        context = {
            'current_patient': current_patient,
            'queue_state': queue_state,
            'medical_records': medical_records
        }

    return render (request, 'doctor/index.html', context)
    
