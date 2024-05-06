from django.forms import ModelForm
from .models import Article


class CreateArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'is_premium', ]
