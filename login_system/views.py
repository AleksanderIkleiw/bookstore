from .send_mail import send__email
import base64
import binascii

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm
from .tokens import account_activation_token, create_url


def extract_and_display_errors(request, form):  # extracts all errors from request and pass it as message
    for error_key in form.errors.keys():
        for error in form.errors[error_key]:
            messages.error(request, error)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)  # we create a loginform and insert post request's data
        if form.is_valid():  # if form is valid we login the user
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user.is_active:  # if user is active(verified) we can log him in
                messages.success(request, 'You have been successfully logged in.')
                login(request, user)

            return redirect('home_page')

    else:
        form = LoginForm()

    extract_and_display_errors(request, form)

    return render(request, 'login_system/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:  # if user is logged, he can't register
        messages.error(request, "You are already logged in.")
        return redirect('home_page')
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False  # we set user to inactive, which will be changed after he verifies by email
            user.save()  # we save the user

            token = account_activation_token.make_token(user=user)  # we generate the token

            url = create_url(request, token, user.pk)  # we create the url with uid and token
            mail_body = f"You have been successfully registered. To activate your account click the link below:\n{url}"
            subject = 'Verification email from Bookstore'
            send__email(form.cleaned_data['email'], subject, mail_body)

            messages.success(request, 'Successfully registered. Check your mail and verify your account.')

            return redirect('home_page')

    else:
        form = RegisterForm()

    extract_and_display_errors(request, form)

    return render(request, 'login_system/register.html', {'form': form})


@login_required
def logout_view(request):
    messages.success(request, "You have been successfully logged out")
    logout(request)
    return redirect('home_page')


def activate_view(request, base64_string):
    try:
        decoded = base64.b64decode(base64_string).decode('ascii')  # we decode base64 string

    except binascii.Error as E:  # we check if the link is a valid base64 string
        messages.error(request, 'Activation URL is invalid.')
        return render(request, 'login_system/base.html')

    uid, token = decoded.split('|')  # I used ,,|'' as a separator, because we need uid to know which user we want to verify
    user = User.objects.get(id=uid)

    if user is not None and account_activation_token.check_token(user, token):  # if user exsits and token is correct we activate user
        user.is_active = True
        user.save()
        messages.success(request, 'You have verified your account successfully. Now you have to log in.')

        return redirect('login_page')
    messages.error(request, 'Activation URL is invalid')
    return redirect('home_page')