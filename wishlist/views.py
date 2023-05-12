from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View


from .wishlist import Wishlist
from store.models import ProductVariant


def summary(request):
    return render(request, 'wishlist/summary.html')


class ModifyWishlist(View):
    def post(self, request):
        wishlist = Wishlist(request)
        product_id = int(request.POST.get('product_id'))
        product_size = request.POST.get('product_size')
        product_color_id = request.POST.get('product_color_id')
        product = get_object_or_404(ProductVariant, product__id=product_id, color=product_color_id, size=product_size)

        if request.POST.get('action') == 'add':
            wishlist.add(product)
            context = {
                'wishlist_qty': len(wishlist)
            }
            response = JsonResponse(context)
            return response

        if request.POST.get('action') == 'delete':
            wishlist.delete(product)
            context = {
                'wishlist_qty': len(wishlist)
            }
            response = JsonResponse(context)
            return response
