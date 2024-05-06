from django.urls import path
from . import views

urlpatterns = [
    path('writer-dashbored', views.writer_dashbored, name='writer-dashbored'),
    path('create-article', views.create_article, name='create-article')

]
