from django.db import models
from account.models import CustomUser


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField(max_length=100000)
    date_post = models.DateTimeField(auto_now_add=True)

    is_premium = models.BooleanField(default=False, verbose_name='IS this a premium article?')
    # verbose is the human-readable name in the form or the databese

    user = models.ForeignKey(CustomUser, max_length=50, on_delete=models.CASCADE, null=True)

    # on_delete=models.CASCADE if the user deletes their account and deletes this article from the database
