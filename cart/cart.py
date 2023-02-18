from store.models import Product

from decimal import Decimal


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.total_qty = 0
        self.total_price = 0
        if 'userdata' not in self.session:
            self.cart = self.session['userdata'] = {}
            return
        self.cart = self.session.get('userdata')

        if self.cart:
            self.count_total_price()
            return

    def add(self, product: Product, product_qty: int):
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_qty': product_qty,
                'product_price': str(product.price),
                'product_name': product.name,
                'product_slug': product.slug
            }
            self.save()
            self.total_qty += product_qty
            return
        
        self.cart[product_id]['product_qty'] += product_qty
        self.save()
        self.total_qty += product_qty


    def update_qty(self, product: Product, product_qty: int):
        product_id = str(product.id)
        self.total_qty -= self.cart[product_id]['product_qty']
        self.total_qty += product_qty

        if product_id in self.cart:
            self.cart[product_id]['product_qty'] = product_qty
            self.save()


    def delete(self, product: Product):
        product_id = str(product.id)
        self.total_qty -= self.cart[product_id]['product_qty']
        
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
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart['product_qty'] = self.cart[str(product.id)]['product_qty']
            cart['product_price'] = str(product.price)
            cart['product_subtotal'] = product.price*self.cart[str(product.id)]['product_qty']
            cart['product_name'] = product.name
            cart['product_description'] = product.description
            cart['product_image'] = product.image
            cart['product_slug'] = product.slug
            cart['product_id'] = product.id
            yield cart
        

    def __len__(self):
        return sum(item['product_qty'] for item in self.cart.values())
