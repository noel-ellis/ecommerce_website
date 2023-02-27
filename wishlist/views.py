from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .wishlist import Wishlist
from store.models import Product


def summary(request):
    return render(request, 'wishlist/summary.html')

def modify(request):
    wishlist = Wishlist(request)
    product_id = int(request.POST.get('product_id'))
    product = get_object_or_404(Product, id=product_id)

    if request.POST.get('action') == 'add':
        wishlist.add(product)
        response = JsonResponse({'wishlist_qty': len(wishlist)})
        return response

    if request.POST.get('action') == 'delete':
        wishlist.delete(product)
        response = JsonResponse({'wishlist_qty': len(wishlist)})
        return response
