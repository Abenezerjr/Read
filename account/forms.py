from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


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
