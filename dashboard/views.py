from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient

@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def view_pacients(request):
    patients = Patient.objects.all().order_by('name')
    context = {
        'patients': patients,
    }

    return render(request, 'pacients.html', context=context)

@login_required
def add_pacient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
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

    return redirect('view_pacients')


