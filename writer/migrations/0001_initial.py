# Generated by Django 5.0.4 on 2024-05-02 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('content', models.TextField(max_length=100000)),
                ('date_post', models.DateTimeField(auto_now_add=True)),
                ('is_premium', models.BooleanField(default=False, verbose_name='IS this a premium article?')),
                ('user', models.ForeignKey(max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
