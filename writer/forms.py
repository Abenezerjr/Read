from django.forms import ModelForm
from .models import Article


class CreateArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'is_premium', ]

    def __init__(self, *args, **kwargs):
        super(CreateArticleForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'textarea'})

