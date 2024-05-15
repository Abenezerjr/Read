from django.forms import ModelForm
from account.models import CustomUser


class ClientAccountManagementForm(ModelForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', ]
        exclude = ['password1', 'password2', ]

    def __init__(self, *args, **kwargs):
        super(ClientAccountManagementForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'placeholder': 'Enter you Email Address'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'FirstName'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'LastName'})
