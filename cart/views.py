from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from store.models import Product, ProductVariant


def summary(request):
    return render(request, 'cart/summary.html')


def modify(request):
    cart = Cart(request)
    product_id = int(request.POST.get('product_id'))
    product_size = request.POST.get('product_size')
    product_color_id = request.POST.get('product_color_id')
    selected_product_variant = ProductVariant.objects.get(size=product_size, color_id=product_color_id)
    product = get_object_or_404(Product, id=selected_product_variant.product.id)

    if request.POST.get('action') == 'add':
        product_qty = int(request.POST.get('product_qty'))
        cart.add(product_variant=selected_product_variant, product_qty=product_qty)

        total_price = cart.count_total_price()
        cart_qty = cart.__len__()
        context = {
            'qty': cart.cart[str(selected_product_variant.id)]['product_qty'],
            'totalqty': cart_qty,
            'totalprice': total_price,
            'img_url': selected_product_variant.image.url,
            'size': selected_product_variant.size,
            'color_name': selected_product_variant.color.name,
        }
        response = JsonResponse(context)
        return response
    
    if request.POST.get('action') == 'delete':
        cart.delete(product=selected_product_variant)

        total_price = cart.count_total_price()
        cart_qty = cart.__len__()
        response = JsonResponse({'totalqty': cart_qty, 'totalprice': total_price})
        return response

    if request.POST.get('action') == 'update':
        product_qty = int(request.POST.get('product_qty'))
        cart.update_qty(product_variant=selected_product_variant, product_qty=product_qty)
        
        subtotal_price = product.price*product_qty
        total_price = cart.count_total_price()
        cart_qty = cart.__len__()
        response = JsonResponse({'qty': product_qty, 'totalqty': cart_qty, 'totalprice': total_price, 'subtotalprice': subtotal_price})
        return response
        
    

    