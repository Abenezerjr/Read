from django.shortcuts import render, redirect
from writer.models import Article
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from client.models import Subscription
from django.core.exceptions import ValidationError
from .forms import ClientAccountManagementForm
from account.models import CustomUser
from .paypal import *


# Create your views here.

@login_required(login_url='login')
def client_dashboard(request):
    try:
        subDetails = Subscription.objects.get(user=request.user)
        subscription_plan = subDetails.subscription_plan
        subscription_id = subDetails.paypal_subscription_id
        context = {'SubPlan': subscription_plan,
                   'SubscriptionID': subscription_id,
                   }
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


@login_required(login_url='login')
def subscription_locked(request):
    return render(request, 'client/subscription-locked.html')


@login_required(login_url='login')
def subscription_plans(request):
    if not Subscription.objects.filter(user=request.user).exists():
        return render(request, 'client/subscription-plans.html')
    else:
        return redirect('client-dashboard')


@login_required(login_url='login')
def client_account_management(request):
    try:
        form = ClientAccountManagementForm(instance=request.user)

        if request.method == 'POST':
            form = ClientAccountManagementForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('client-dashboard')

        subDetails = Subscription.objects.get(user=request.user)

        subscription_id = subDetails.paypal_subscription_id
        subscription_plan = subDetails.subscription_plan
        context = {
            # 'form': form,
            'SubscriptionID': subscription_id,
            'SubPlan': subscription_plan,
            'form': form
        }
        return render(request, 'client/account-management.html', context)
    except:
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


def delete_account(request):
    if request.method == "POST":
        delete_user = CustomUser.objects.get(email=request.user)
        delete_user.delete('')

        return redirect('register')

    return render(request, '#')


@login_required(login_url='login')
def create_subscription(request, subID, plan):
    custom_user = CustomUser.objects.get(email=request.user)
    if not Subscription.objects.filter(user=request.user).exists():
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
    else:
        return redirect('client-dashboard')


@login_required(login_url='login')
def delete_subscription(request, subID):
    # delete subscription from paypal
    try:
        access_token = get_access_token()

        cancel_subscription_paypal(access_token, subID)

        # Delete a subscription from Django application
        subscription = Subscription.objects.get(user=request.user, paypal_subscription_id=subID)

        subscription.delete()
        return render(request, 'client/delete_subscription.html')
    except:
        return redirect('client-dashboard')


@login_required(login_url='login')
def update_subscription(request, subID):
    access_token = get_access_token()

    approve_link = update_subscription_paypal(access_token, subID)

    if approve_link:
        return redirect(approve_link)
    else:
        return HttpResponse("unable to obtain the approval link")


@login_required(login_url='login')
def paypal_update_sub_confirmed(request):
    try:
        subDetails = Subscription.objects.get(user=request.user)
        subscriptionID = subDetails.paypal_subscription_id

        context = {
            'subscriptionID': subscriptionID
        }

        return render(request, 'client/paypal-update-sub-confiremd.html', context)
    except:
        return render(request, 'client/paypal-update-sub-confiremd.html')


def app_update_sub_confirmed(request, subID):
    access_token = get_access_token()
    current_plan_id = get_current_subscription(access_token, subID)

    if current_plan_id == 'P-7064205047605035BMZCITBQ':
        new_plan_name = 'Standard'
        new_plan_cost = "4.99"

        Subscription.objects.filter(paypal_subscription_id=subID).update(subscription_plan=new_plan_name
                                                                         , subscription_cost=new_plan_cost)

    elif current_plan_id == 'P-7RA300099Y398215DMZCI5KA':
        new_plan_name = 'Premium'
        new_plan_cost = "9.99"

        Subscription.objects.filter(paypal_subscription_id=subID).update(subscription_plan=new_plan_name
                                                                         , subscription_cost=new_plan_cost)

    return render(request, 'client/app-update-sub-confirem.html')
