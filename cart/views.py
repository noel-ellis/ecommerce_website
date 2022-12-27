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
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        response = JsonResponse({'test': 'data'})
        return response

    