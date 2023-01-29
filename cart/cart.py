from store.models import Product

from decimal import Decimal


class Cart:
    """
    Base Cart Class
    """

    def __init__(self, request):
        self.session = request.session
        if 'userdata' not in self.session:
            self.cart = self.session['userdata'] = {}
            return
        self.cart = self.session.get('userdata')

        if self.cart:
            self.total = self.count_total()

    def add(self, product: Product, product_qty: int):
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_qty': product_qty,
                'product_price': str(product.price),
                'product_name': product.name,
                'product_slug': product.slug
            }
            # Updates DB w/ cart data
            self.session.modified = True
            return
        
        self.cart[product_id]['product_qty'] += product_qty

        # Updates DB w/ cart data
        self.session.modified = True

    def delete(self, product: Product):
        product_id = str(product.id)
        
        if product_id in self.cart:
            del self.cart[product_id]
            # Updates DB w/ cart data
            self.session.modified = True
            return

        # Updates DB w/ cart data
        self.session.modified = True
        

    def count_total(self):
        total = 0
        for item in self.cart.values():
            total += int(item['product_qty'])*Decimal(item['product_price'])

        return total
    

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart['product_qty'] = self.cart[str(product.id)]['product_qty']
            cart['product_price'] = str(product.price)
            cart['product_name'] = product.name
            cart['product_slug'] = product.slug
            cart['product_id'] = product.id
            yield cart
        

    def __len__(self):
        return sum(item['product_qty'] for item in self.cart.values())