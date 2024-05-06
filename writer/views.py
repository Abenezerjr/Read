from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateArticleForm
from .models import Article


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
    return render(request, 'writer/my-article.html',context)
