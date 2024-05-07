from django.shortcuts import render, redirect
from writer.models import Article
from django.contrib.auth.decorators import login_required
from .models import Subscription
from django.core.exceptions import ValidationError


# Create your views here.

@login_required(login_url='login')
def client_dashboard(request):
    return render(request, 'client/client-dashbored.html')


@login_required(login_url='login')
def read_article(request):
    # articles=None
    try:
        subDetails = Subscription.objects.get(user=request.user, is_active=True)
    except:
        # articles = None
        return redirect('subscription_locked')

    current_subscription_plan = subDetails.subscription_plan

    if current_subscription_plan == 'Standard':
        articles = Article.objects.all().filter(is_premium=False)
    elif current_subscription_plan == 'Premium':
        articles = Article.objects.all()

    context = {
        'articles': articles
    }
    return render(request, 'client/read-article.html', context)


def subscription_locked(request):
    return render(request,'client/subscription-locked.html')