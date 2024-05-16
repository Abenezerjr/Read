import requests
import json
from django.conf import settings

from .models import Subscription


def get_access_token():
    data = {'grant_type': 'client_credentials'}

    headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}

    client_id = settings.SS_CLIENT_ID
    secret_id = settings.SS_SECRET_ID

    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'

    r = requests.post(url, auth=(client_id, secret_id), headers=headers, data=data).json()

    access_token = r['access_token']

    return access_token


def cancel_subscription_paypal(access_token, subID):
    bearer_token = 'Bearer ' + access_token

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subID + '/cancel'

    r = requests.post(url, headers=headers)

    print(r.status_code)


def update_subscription_paypal(access_token, subID):
    bearer_token = 'Bearer ' + access_token

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    subDetails = Subscription.objects.get(paypal_subscription_id=subID)

    current_subscription_plan = subDetails.subscription_plan

    if current_subscription_plan == 'Standard':
        new_subscription_plan_id = 'P-7RA300099Y398215DMZCI5KA'  # to Premium
    elif current_subscription_plan == 'Premium':
        new_subscription_plan_id = 'P-7064205047605035BMZCITBQ'  # to Standard

    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subID + '/revise'

    revision_data = {
        'plan_id': new_subscription_plan_id,
    }

    r = requests.post(url, headers=headers, data=json.dumps(revision_data))
    """
   json.dumps: Python object into a JSON string
    """

    response_data = r.json()
    print(response_data)

    approve_link = None

    for link in response_data.get('links', []):
        if link.get('rel') == 'approve':
            approve_link = link['href']

    if r.status_code == 200:

        print("request was a success")

        return approve_link

    else:
        print('sorry,an error occurred!')


def get_current_subscription(access_token, subIO):
    bearer_token = 'Bearer ' + access_token

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    url = f'https://api.sandbox.paypal.com/v1/billing/subscriptions/{subIO}'

    r= requests.get(url,headers=headers)
    if r.status_code == 200:
        subscription_data=r.json()

        current_plan_id=subscription_data.get('plan_id')

        return current_plan_id
    else:
        print("Failed to retrieve subscription details")

        return None

