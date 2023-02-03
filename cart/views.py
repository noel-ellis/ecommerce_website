from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from store.models import Product


def summary(request):
    return render(request, 'cart/summary.html')


def checkout(request):
    return render(request, 'cart/checkout.html')


def modify(request):
    cart = Cart(request)
    product_id = int(request.POST.get('productid'))
    product = get_object_or_404(Product, id=product_id)

    if request.POST.get('action') == 'add':
        product_qty = int(request.POST.get('productqty'))
        cart.add(product=product, product_qty=product_qty)
        total_price = cart.count_total()
        cart_qty = cart.__len__()
        response = JsonResponse({'qty': cart.cart[str(product_id)]['product_qty'], 'totalqty': cart_qty, 'productslug': product.slug, 'totalprice': total_price})
    
    if request.POST.get('action') == 'delete':
        cart.delete(product=product)
        total_price = cart.count_total()
        cart_qty = cart.__len__()
        response = JsonResponse({'productslug': product.slug, 'totalprice': total_price, 'totalqty': cart_qty})

    if request.POST.get('action') == 'update':
        product_qty = int(request.POST.get('productqty'))
        cart.update_qty(product=product, product_qty=product_qty)
        
        subtotalprice = product.price*product_qty
        total_price = cart.count_total()
        response = JsonResponse({'totalprice': total_price, 'subtotalprice': subtotalprice})
        
    return response

    