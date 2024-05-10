from django.shortcuts import render, redirect
from writer.models import Article
from django.contrib.auth.decorators import login_required
from .models import Subscription
from django.core.exceptions import ValidationError
from .forms import ClientAccountManagementForm
from account.models import CustomUser


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


def create_subscription(request, subID, plan):
    custom_user = CustomUser.objects.get(email=request.user)
    firstName = custom_user.first_name
    lastName = custom_user.last_name

    fullName = firstName + ' ' + lastName

    selected_sub_plan = plan
    if selected_sub_plan == 'Standard':
        sub_cost = 4.99
    elif selected_sub_plan == 'Premium':
        sub_cost = 9.99

    subscription = Subscription.objects.create(
        subscriber_name=fullName,
        subscription_plan=selected_sub_plan,
        subscription_cost=sub_cost,
        paypal_subscription_id=subID,
        is_active=True,
        user=request.user
    )
    context = {
        "subscriptionPlan": selected_sub_plan
    }

    return render(request, 'client/create-subscription.html', context)
