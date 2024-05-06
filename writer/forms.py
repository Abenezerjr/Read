from django.forms import ModelForm
from .models import Article
from account.models import CustomUser


class CreateArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'is_premium', ]

    def __init__(self, *args, **kwargs):
        super(CreateArticleForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'textarea'})


class UpdateUserForm(ModelForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', ]
        exclude = ['password1', 'password2', ]

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'placeholder': 'Enter you Email Address'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'FirstName'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'LastName'})
