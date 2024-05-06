from django.urls import path
from . import views

urlpatterns = [
    path('writer-dashbored', views.writer_dashbored, name='writer-dashbored'),
    path('create-article', views.create_article, name='create-article'),
    path('my_articles', views.my_articles, name='my_articles'),
    path('update_article/<str:pk>/', views.update_article, name='update-article'),
    path('delete_article/<str:pk>/', views.delete_article, name='delete_article'),


]
