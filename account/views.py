from django.shortcuts import render, HttpResponse


# Create your views here.

def home(request):
    return render(request, 'index.html')


def UserRegister(request):
    return render(request,'account/register.html')


def UserLogin(request):
    return render(request,'account/login.html')
