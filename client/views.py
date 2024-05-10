from django.shortcuts import render, redirect
from writer.models import Article
from django.contrib.auth.decorators import login_required
from .models import Subscription
from django.core.exceptions import ValidationError
from .forms import ClientAccountManagementForm


# Create your views here.

@login_required(login_url='login')
def client_dashboard(request):
    try:
        subDetails = Subscription.objects.get(user=request.user)
        subscription_plan = subDetails.subscription_plan
        context = {'SubPlan': subscription_plan}
        return render(request, 'client/client-dashbored.html', context)
    except:
        subscription_plan = 'None'
        context = {'SubPlan': subscription_plan}
        return render(request, 'client/client-dashbored.html', context)


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
    return render(request, 'client/subscription-locked.html')


def subscription_plans(request):
    return render(request, 'client/subscription-plans.html')


def client_account_management(request):
    form = ClientAccountManagementForm(instance=request.user)

    if request.method == 'POST':
        form = ClientAccountManagementForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('client-dashboard')

    context = {
        'form': form
    }
    return render(request, 'client/account-management.html', context)
