from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def writer_dashbored(request):
    return render(request, 'writer/writer-dashbored.html')
