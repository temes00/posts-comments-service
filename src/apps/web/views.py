
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import AuthForm, RegistrationForm
from .utils import generate_user_auth_hash

# Create your views here.


def root(request):
    return render(request, 'root.html')


@login_required(login_url='/auth')
def profile(request):
    return HttpResponse('You are welcome!', status=200)


def auth(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('root')
            else:
                return HttpResponse('Data is invalid!')
    else:
        form = AuthForm()
    return render(request, 'auth.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                is_active=False,
            )
            messages.add_message(
                request,
                messages.INFO,
                'Registration completed successfully.'
            )
            user_hash = generate_user_auth_hash(
                user_id=user.pk,
                user_name=user.username,
            )
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('mails/confirm_email.html', {
                'first_name': f'{user.first_name}',
                'last_name': f'{user.last_name}',
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_hash,
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, '', [to_email])
            messages.add_message(
                request,
                messages.INFO,
                'We have sent you a confirmation email.'
            )
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if (
        user is not None and
        generate_user_auth_hash(
            user_id=user.pk,
            user_name=user.username
        ) == token
    ):
        user.is_active = True
        user.save()
        return HttpResponse(
            'Thank you for your email confirmation. '
            'Now you can login your account.'
        )
    else:
        return HttpResponse('Activation link is invalid!')


def log_out(request):
    logout(request)
    return redirect('root')
