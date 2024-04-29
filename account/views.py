from django.shortcuts import render, HttpResponse

from .forms import CreatUserForm


# Create your views here.

def home(request):
    return render(request, 'account/index.html')


def UserRegister(request):
    form = CreatUserForm()
    if request.method == "POST":
        form = CreatUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('user is register')

    context = {
        'RegisterForm': form
    }
    return render(request, 'account/register.html', context)


def UserLogin(request):
    return render(request, 'account/login.html')
