from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from main.models import User
from django.contrib.auth.decorators import login_required


def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_conf = request.POST['password_conf']
        if password == password_conf:
            User.objects.create_user(username=username, password=password, email=email)

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)

            return redirect('front:index')
        else:
            return redirect('auth:error')

    return render(request, 'dashboard/auth/sign-up.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('front:index')

        else:
            return redirect('auth:error')

    return render(request, 'dashboard/auth/login.html')


def log_out(request):
    logout(request)
    return redirect('front:index')
