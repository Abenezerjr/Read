from django.shortcuts import render, HttpResponse, redirect

from .forms import CreatUserForm

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login, logout, authenticate


# Create your views here.

def home(request):
    return render(request, 'account/index.html')


def UserRegister(request):
    form = CreatUserForm()
    if request.method == "POST":
        form = CreatUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

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
