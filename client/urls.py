from django.urls import path
from . import views

urlpatterns = [
    path('client-dashboard', views.client_dashboard, name='client-dashboard'),
    path('read-article/', views.read_article, name='read-article'),
    path('subscription_locked/', views.subscription_locked, name='subscription_locked'),
]
