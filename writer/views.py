from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateArticleForm
from .models import Article
from django.core.exceptions import PermissionDenied


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
    article = Article.objects.get(id=pk, user=request.user)

    if request.method == 'POST':
        article.delete()
        return redirect('my_articles')

    context = {
        'article': article
    }
    return render(request, 'writer/delete-article.html', context)
