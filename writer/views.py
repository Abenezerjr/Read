from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CreateArticleForm


# Create your views here.

@login_required(login_url='login')
def writer_dashbored(request):
    return render(request, 'writer/writer-dashbored.html')


def create_article(request):
    form = CreateArticleForm()
    # user = request.user
    if request.method == "POST":
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user  # this is the user currently sign in
            article.save()
            return HttpResponse('Article is created')

    context = {
        'form': form
    }
    return render(request, 'writer/create-article.html', context)
