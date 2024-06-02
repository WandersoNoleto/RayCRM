from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient
from django.contrib import messages
from django.http import JsonResponse
import json
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404

@login_required
def home(request):
    return render(request, 'index.html')

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