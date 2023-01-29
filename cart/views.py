from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from store.models import Product

# Create your views here.
def summary(request):
    return render(request, 'store/cart/summary.html')


def modify(request):
    cart = Cart(request)
    product_id = int(request.POST.get('productid'))
    product = get_object_or_404(Product, id=product_id)

    if request.POST.get('action') == 'add':
        product_qty = int(request.POST.get('productqty'))
        cart.add(product=product, product_qty=product_qty)
        cart_qty = cart.__len__()
        response = JsonResponse({'qty': cart.cart[str(product_id)]['product_qty'], 'totalqty': cart_qty, 'productslug': product.slug})

        return response
    
    if request.POST.get('action') == 'delete':
        cart.delete(product=product)
        response = JsonResponse({'productslug': product.slug})
        
        return response

    