import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

from ecommerce_website.settings import STRIPE_API_SECRET_KEY

from cart.cart import Cart
from users.models import DeliveryInfo
from orders.views import payment_confirmation
from users.forms import UserUpdateForm
from users.models import UserBase

import stripe


@login_required
def checkout(request):
    cart = Cart(request)
    user_info = UserBase.objects.filter(id=request.user.id).first()
    address_info = DeliveryInfo.objects.filter(user=request.user.id).all()

    # Convert float to a Stripe-specific int format (same float but w/o the dot: 10.99 -> 1099)
    total_price = str(cart.count_total_price())
    total_price = total_price.replace('.', '')
    total_price = int(total_price)

    stripe.api_key = STRIPE_API_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total_price,
        currency='usd',
        metadata={'userid': request.user.id}
    )

    context = {
        'client_secret': intent.client_secret,
        'address_info': address_info,
        'user_info': user_info
    }
    return render(request, 'payment/checkout.html', context)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)
