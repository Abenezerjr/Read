from django.shortcuts import render, HttpResponse


# Create your views here.

def writer_dashbored(request):
    return render(request,'writer/writer-dashbored.html')
