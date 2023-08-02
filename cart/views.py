from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views import View

from .cart import Cart
from store.models import Product, ProductVariant


def summary(request):
    return render(request, 'cart/summary.html')


class ModifyCart(View):
    def post(self, request):
        action = request.POST.get('action')

        if action == 'add':
            return self.add_to_cart(request)
        if action == 'delete':
            return self.delete_from_cart(request)
        if action == 'update':
            return self.update_cart(request)

    def get_product_variant(self, request):
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        product_size = request.POST.get('product_size')
        product_color_id = request.POST.get('product_color_id')
        selected_product_variant = get_object_or_404(ProductVariant,
                                                     product=product, size=product_size, color_id=product_color_id)
        return selected_product_variant

    def count_subtotal_price(self, request):
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        product_qty = int(request.POST.get('product_qty'))
        return product.price*product_qty

    def add_to_cart(self, request):
        cart = Cart(request)
        selected_product_variant = self.get_product_variant(request)

        product_qty = int(request.POST.get('product_qty'))
        if selected_product_variant.available_units < product_qty:
            raise Http404
        cart.add(product_variant=selected_product_variant,
                 product_qty=product_qty)

        total_price = cart.count_total_price()
        cart_qty = cart.__len__()
        context = {
            'qty': cart.product_qty(selected_product_variant),
            'product_variant_id': selected_product_variant.id,
            'totalqty': cart_qty,
            'totalprice': total_price,
            'img_url': selected_product_variant.image.url,
            'size': selected_product_variant.size,
            'color_name': selected_product_variant.color.name,
        }
        response = JsonResponse(context)
        return response

    def delete_from_cart(self, request):
        cart = Cart(request)
        selected_product_variant = self.get_product_variant(request)
        cart.delete(product_variant=selected_product_variant)

        total_price = cart.count_total_price()
        cart_qty = cart.__len__()
        context = {
            'product_variant_id': selected_product_variant.id,
            'totalqty': cart_qty,
            'totalprice': total_price
        }
        response = JsonResponse(context)
        return response

    def update_cart(self, request):
        cart = Cart(request)
        selected_product_variant = self.get_product_variant(request)
        product_qty = int(request.POST.get('product_qty'))
        if selected_product_variant.available_units < product_qty:
            raise Http404
        cart.update_qty(product_variant=selected_product_variant,
                        product_qty=product_qty)

        subtotal_price = self.count_subtotal_price(request)
        total_price = cart.count_total_price()
        cart_qty = cart.__len__()
        response = JsonResponse({'qty': product_qty, 'totalqty': cart_qty,
                                'totalprice': total_price, 'subtotalprice': subtotal_price})
        return response
