from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import NextConsultDate, PaymentMethods
from appointments.models import Appointment
from patients.models import Patient
from django.db.models.functions import Lower

@login_required
def home(request):
    next_consult_date = NextConsultDate.objects.all().first()
    patients = Patient.objects.filter(clinic=request.user.clinic).order_by(Lower('name'))
    appointments = Appointment.objects.filter
    payment_methods = PaymentMethods.objects.all()

    context = {
        'patients': patients,
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