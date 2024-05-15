from django.urls import path
from . import views

urlpatterns = [
    path('client-dashboard', views.client_dashboard, name='client-dashboard'),
    path('read-article/', views.read_article, name='read-article'),
    path('subscription_locked/', views.subscription_locked, name='subscription_locked'),
    path('subscription_plans/', views.subscription_plans, name='subscription_plans'),
    path('client-account-management/', views.client_account_management, name='client_account_management'),
    path('create-subscription/<subID>/<plan>', views.create_subscription, name='create-subscription'),
    path('delete-subscription/<subID>', views.delete_subscription, name='delete-subscription'),
    path('update-subscription/<subID>', views.update_subscription, name='update-subscription'),
    path('paypal-update-sub-confirmed/', views.paypal_update_sub_confirmed, name='paypal_update_sub_confirmed'),
]
