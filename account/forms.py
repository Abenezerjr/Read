from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import CustomUser


class StyledAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Password'
        })
    )


class CreatUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'is_writer']
        labels = {
            'is_writer': 'Are You a Writer? ',
        }

    def __init__(self, *args, **kwargs):
        super(CreatUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'placeholder': 'Enter you Email Address'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'FirstName'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'LastName'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter Your Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Your Password'})
        self.fields['is_writer'].widget.attrs.update({'label': 'are You a writer?'})
