from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import Order, OrderedItem
from django.http import JsonResponse

def new_order(request):
    if request.POST:
        user_id = request.user.id
        delivery_info_id = request.POST.get('delivery_info_id')
        status = 'ST1'
        # ISSUE: creates same orders over and over again
        new_order = Order.objects.create(user_id=user_id, delivery_info_id=delivery_info_id, status=status)

        ordered_item_ids = []
        cart = Cart(request)
        products_in_cart = cart.cart
        
        for id, data in products_in_cart.items():
            ordered_item = OrderedItem.objects.create(product_id=id, quantity=data['product_qty'], price=data['product_price'])
            ordered_item.save()
            ordered_item_ids.append(ordered_item.id)

        new_order.ordered_items.set(ordered_item_ids)
        new_order.save()

    response = JsonResponse({'status':'OK'})
    return response

