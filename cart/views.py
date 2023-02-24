from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from store.models import Product


def summary(request):
    return render(request, 'cart/summary.html')


def modify(request):
    cart = Cart(request)
    product_id = int(request.POST.get('product_id'))
    product = get_object_or_404(Product, id=product_id)

    if request.POST.get('action') == 'add':
        product_qty = int(request.POST.get('product_qty'))
        cart.add(product=product, product_qty=product_qty)

        total_price = cart.count_total_price()
        cart_qty = cart.__len__()
        response = JsonResponse({'qty': cart.cart[str(product_id)]['product_qty'], 'totalqty': cart_qty, 'totalprice': total_price})
        return response
    
    if request.POST.get('action') == 'delete':
        cart.delete(product=product)

        total_price = cart.count_total_price()
        cart_qty = cart.__len__()
        response = JsonResponse({'totalqty': cart_qty, 'totalprice': total_price})
        return response

    if request.POST.get('action') == 'update':
        product_qty = int(request.POST.get('product_qty'))
        cart.update_qty(product=product, product_qty=product_qty)
        
        subtotal_price = product.price*product_qty
        total_price = cart.count_total_price()
        cart_qty = cart.__len__()
        response = JsonResponse({'qty': product_qty, 'totalqty': cart_qty, 'totalprice': total_price, 'subtotalprice': subtotal_price})
        return response
        
    

    