from store.models import Product, ProductVariant

from decimal import Decimal


class Cart:
    def __init__(self, request):
        self.session_cart_name = 'cart'
        self.session = request.session
        
        # Get cart data or create new cart
        if self.session_cart_name not in self.session:
            self.cart = self.session[self.session_cart_name] = {}
            return
        self.cart = self.session.get(self.session_cart_name)

        self.total_price = 0
        if self.cart:
            self.count_total_price()
            return

    def add(self, product_variant: ProductVariant, product_qty: int):
        product_variation_id = str(product_variant.id)
        product_price = str(product_variant.product.price)
        product_name = str(product_variant.product.name)
        product_slug = str(product_variant.product.slug)
        
        if product_variation_id not in self.cart:
            self.cart[product_variation_id] = {
                'product_qty': product_qty,
                'product_price': product_price,
                'product_name': product_name,
                'product_slug': product_slug,
            }
            self.save()
            return
        
        self.cart[product_variation_id]['product_qty'] += product_qty
        self.save()

    def update_qty(self, product_variant: ProductVariant, product_qty: int):
        product_id = str(product_variant.id)

        if product_id in self.cart:
            self.cart[product_id]['product_qty'] = product_qty
            self.save()

    def delete(self, product_variant: ProductVariant):
        product_id = str(product_variant.id)
        
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            return
        self.save()

    def count_total_price(self):
        self.total_price = 0
        for item in self.cart.values():
            self.total_price += int(item['product_qty'])*Decimal(item['product_price'])

        return self.total_price

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_variant_ids = self.cart.keys()
        products = ProductVariant.objects.filter(id__in=product_variant_ids)
        cart = self.cart.copy()
        
        for product_variant in products:
            cart['product_qty'] = self.cart[str(product_variant.id)]['product_qty']
            cart['product_price'] = str(product_variant.product.price)
            cart['product_subtotal'] = product_variant.product.price*self.cart[str(product_variant.id)]['product_qty']
            cart['product_name'] = product_variant.product.name
            cart['product_description'] = product_variant.product.description
            cart['product_image'] = product_variant.image
            cart['product_slug'] = product_variant.product.slug
            cart['product_id'] = product_variant.product.id
            cart['product_variant_id'] = product_variant.id
            cart['product_color'] = product_variant.color
            cart['product_color_id'] = product_variant.color.id
            cart['product_size'] = product_variant.size
            cart['product_availability'] = False
            if product_variant.available_units > 0:
                cart['product_availability'] = True
            
            yield cart        

    def __len__(self):
        return sum(item['product_qty'] for item in self.cart.values())
    
    def clear(self):
        del self.session[self.session_cart_name]
        self.save()
