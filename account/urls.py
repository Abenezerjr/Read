from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name=''),
    path('register/', views.UserRegister, name='register'),
    path('login/', views.UserLogin, name='login'),
    path('logout/', views.UserLogout, name='logout'),
    path('about/', views.about, name='about'),

    # password management

    # URL patterns for password management
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),
         name='reset_password'),

    # Show a success message stating that an email was sent to reset our password
    path('reset_password_done',
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'),
         name='password_reset_confirm'),

    # Show a success message stating that our password was changed
    path('reset_password_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),

    # Email Verification

    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),
    path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),
    path('email-verification-success', views.email_verification_success, name='email-verification-success'),
    path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),

]
