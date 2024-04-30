from django.urls import path
from . import views

urlpatterns = [
    path('writer-dashbored', views.writer_dashbored, name='writer-dashbored')

]
