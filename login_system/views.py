from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def extract_and_display_errors(request, form):
    for error_key in form.errors.keys():
        for error in form.errors[error_key]:
            messages.error(request, error)


def home_view(request):
    return render(request, 'login_system/base.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user.is_active:
                messages.success(request, 'You have been successfully logged in.')
                login(request, user)

            return redirect('home_page')

    else:
        form = LoginForm()

    extract_and_display_errors(request, form)

    return render(request, 'login_system/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in.")
        return redirect('home_page')
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Successfully registered. You are now logged in.')

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('home_page')

    else:
        form = RegisterForm()

    extract_and_display_errors(request, form)

    return render(request, 'login_system/register.html', {'form': form})


def logout_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You are not logged in.')
        return redirect('home_page')
    messages.success(request, "You have been successfully logged out")
    logout(request)
    return redirect('home_page')
