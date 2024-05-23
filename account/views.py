from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from .forms import CreatUserForm
from django.conf import settings

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from .token import UserVerificationTokenGenerator, user_tokenizer_generate
from .models import CustomUser


# Create your views here.

def home(request):
    return render(request, 'index.html')


def UserRegister(request):
    form = CreatUserForm()
    if request.method == "POST":
        form = CreatUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)

            subject = 'Activate Your account'

            message = render_to_string('account/email-verification.html', {

                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user)

            })

            user_email = user.email

            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[user_email])

            return redirect('email-verification-sent')

        # email verification

    context = {
        'RegisterForm': form
    }
    return render(request, 'account/register.html', context)


def UserLogin(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_writer == True:
                login(request, user)
                return redirect('writer-dashbored')
            if user is not None and user.is_writer == False:
                login(request, user)
                return redirect('client-dashboard')
    context = {
        'loginForm': form
    }

    return render(request, 'account/login.html', context)


def UserLogout(request):
    logout(request)
    return redirect('login')


def email_verification(request, uidb64, token):
    unique_token = force_str(urlsafe_base64_decode(uidb64))
    custom_user = CustomUser.objects.get(pk=unique_token)

    if custom_user and user_tokenizer_generate.check_token(custom_user, token):
        custom_user.is_active = True
        custom_user.save()
        return redirect('email-verification-success')
    else:
        return redirect('email-verification-failed')


def email_verification_sent(request):
    return render(request, 'account/email-verification-sent.html')


def email_verification_success(request):
    return render(request, 'account/email-verification-success.html')


def email_verification_failed(request):
    return render(request, 'account/email-verification-failed.html')


def about(request):
    return render(request, 'about -page.html')
