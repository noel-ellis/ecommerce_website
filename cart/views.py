from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from store.models import Product

# Create your views here.
def summary(request):
    return render(request, 'store/cart/summary.html')


def add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_qty)

        cart_qty = cart.__len__()
        response = JsonResponse({'productqty': cart_qty})
        return response

    