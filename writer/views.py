from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateArticleForm, UpdateUserForm
from .models import Article
from django.core.exceptions import PermissionDenied
from account.models import CustomUser


# Create your views here.

@login_required(login_url='login')
def writer_dashbored(request):
    return render(request, 'writer/writer-dashbored.html')


@login_required(login_url='login')
def create_article(request):
    form = CreateArticleForm()
    # user = request.user
    if request.method == "POST":
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user  # this is the user currently sign in
            article.save()
            return redirect('my_articles')

    context = {
        'form': form
    }
    return render(request, 'writer/create-article.html', context)


def my_articles(request):
    current_user = request.user.id
    articles = Article.objects.all().filter(user=current_user)
    context = {
        "articles": articles
    }
    return render(request, 'writer/my-article.html', context)


def update_article(request, pk):
    try:
        current_user = request.user
        article = Article.objects.get(id=pk, user=current_user)
    except PermissionDenied:
        return redirect('my_articles')

    form = CreateArticleForm(instance=article)

    if request.method == "POST":
        form = CreateArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('my_articles')

    context = {
        "form": form
    }
    return render(request, 'writer/update-article.html', context)


def delete_article(request, pk):
    try:
        article = Article.objects.get(id=pk, user=request.user)
    except PermissionDenied:
        return redirect('my_articles')

    if request.method == 'POST':
        article.delete()
        return redirect('my_articles')

    context = {
        'article': article
    }
    return render(request, 'writer/delete-article.html', context)


def account_management(request):
    user = request.user
    form = UpdateUserForm(instance=user)
    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('writer-dashbored')
    context = {
        "form": form
    }

    return render(request, 'writer/account-management.html', context)


def delete_account(request):
    if request.method == 'POST':
        deleteUser = CustomUser.objects.get(email=request.user)

        deleteUser.delete()
        return redirect('login')

    return render(request, 'writer/account-delete.html')
