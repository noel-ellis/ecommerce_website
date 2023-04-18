from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


from cart.cart import Cart
from .models import Order, OrderedItem

@login_required
def new_order(request):
    if request.POST:
        user_id = request.user.id
        delivery_info_id = request.POST.get('delivery_info_id')
        order_key = request.POST.get('order_key')
        status = 'ST1'

        order_quiery = Order.objects.filter(order_key=order_key)
        if not order_quiery.exists():
            new_order = Order.objects.create(user_id=user_id, delivery_info_id=delivery_info_id, paid=False, status=status, order_key=order_key)
            ordered_item_ids = []
            cart = Cart(request)
            products_in_cart = cart.cart
            
            for id, data in products_in_cart.items():
                ordered_item = OrderedItem.objects.create(product_id=id, quantity=data['product_qty'], price=data['product_price'])
                ordered_item.save()
                ordered_item_ids.append(ordered_item.id)

            new_order.ordered_items.set(ordered_item_ids)
            new_order.save()

    response = JsonResponse({'status': 'ok'})
    return response

def orderplaced(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'orders/orderplaced.html')

# Handled through Stripe webhook
# Use this command to activate webhook:
# stripe listen --forward-to localhost:8000/payment/webhook/
def payment_confirmation(order_key):
    order_quiery = Order.objects.filter(order_key=order_key)
    if order_quiery.exists():
        order_quiery.update(paid=True)
