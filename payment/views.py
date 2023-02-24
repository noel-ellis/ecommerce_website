from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ecommerce_website.settings import STRIPE_API_SECRET_KEY

from cart.cart import Cart
from users.forms import DeliveryInfoForm
from users.models import DeliveryInfo

import stripe


@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == "POST":
        form = DeliveryInfoForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Updated')
            return redirect('users:settings')

        messages.error(request, 'Data is invalid')
        return redirect('users:settings')

    address_info = DeliveryInfo.objects.filter(user=request.user.id)

    # Convert float to a Stripe-specific int format (same float but w/o the dot: 10.99 -> 1099)
    total_price = str(cart.count_total_price())
    total_price = total_price.replace('.', '')
    total_price = int(total_price)

    stripe.api_key = STRIPE_API_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount = total_price,
        currency='usd',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/checkout.html', {'client_secret': intent.client_secret, 'address_info': address_info})

def orderplaced(request):
    return render(request, 'payment/orderplaced.html')
