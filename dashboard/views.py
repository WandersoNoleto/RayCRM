from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Patient

@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def view_pacients(request):
    patients =  Patient.objects.all()
    print(patients)
    context = {
        'patients': patients,
    }

    return render(request, 'pacients.html', context=context)



