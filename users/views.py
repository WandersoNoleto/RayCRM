from django.shortcuts import render, redirect
from .models import User
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
            return redirect("home")
    
    return redirect("login")

def register_view(request):
    return render(request, 'register.html')


def user_storage(request):
    if request.method == "POST":
        username = request.POST.get("email")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password
        )

        user.save()

    return redirect("login")