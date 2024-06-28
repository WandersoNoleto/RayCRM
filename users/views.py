from django.shortcuts import render, redirect
from .models import User, Clinic, Receptionist, Doctor
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    return render(request, 'login.html')

def login_check(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(username, password)

        user = authenticate(request, username=username, password=password)

        print(user)
        if user is not None:
            login(request, user)
            if user.user_type == 'receptionist':
                return redirect("home")
            if user.user_type == 'doctor':
                return redirect("doctor_view")
    
    return redirect("login")

def register_choices_view(request):
    return render(request, 'register-choices.html')

def register_doctor_view(request):
    clinics = Clinic.objects.all() 

    context = {
        'clinics': clinics
    }

    return render(request, 'register-doctor.html', context)

def register_doctor(request):
    if request.method == 'POST':
        username = request.POST['email']  
        email = request.POST['email']
        password = request.POST['password']
        clinic_id = request.POST['clinic']  
        phone = request.POST['phone']

        user = User.objects.create_user(username=username, email=email, password=password, user_type="doctor")
        user.save()

        clinic = Clinic.objects.get(id=clinic_id)
        doctor = Doctor.objects.create(user=user, clinic=clinic, phone=phone)
        doctor.save()

        return redirect('login')  
    else:
        clinics = Clinic.objects.all()  
        return render(request, 'registro_doctor.html', {'clinics': clinics})

def register_receptionist_view(request):
    clinics = Clinic.objects.all() 

    context = {
        'clinics': clinics
    }

    return render(request, 'register-receptionist.html', context)


def register_receptionist(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        clinic_id = request.POST['clinic']  

        user = User.objects.create_user(username=email, email=email, password=password, user_type="receptionist")
        user.save()

        clinic = Clinic.objects.get(id=clinic_id)
        receptionist = Receptionist.objects.create(name=name, user=user, clinic=clinic)
        receptionist.save()

        return redirect('login')  
    else:
        clinics = Clinic.objects.all()  
        return render(request, 'registro_receptionista.html', {'clinics': clinics})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        
    return redirect('login')