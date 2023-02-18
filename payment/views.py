import stripe

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from ecommerce_website.settings import STRIPE_API_SECRET_KEY

@login_required
def checkout(request):
    cart = Cart(request)

    # Convert float to a Stripe-specific int format (same float but w/o the dot 10.99 -> 1099)
    total_price = str(cart.count_total_price())
    total_price = total_price.replace('.', '')
    total_price = int(total_price)

    stripe.api_key = STRIPE_API_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount = total_price,
        currency='usd',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/checkout.html', {'client_secret': intent.client_secret})

def orderplaced(request):
    return render(request, 'payment/orderplaced.html')