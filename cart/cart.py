from store.models import Product


class Cart:
    """
    Base Cart Class
    """

    def __init__(self, request):
        self.session = request.session
        if 'skey' not in self.session:
            self.cart = self.session['skey'] = {}
            return
        self.cart = self.session.get('skey')

    def add(self, product: Product, product_qty: int):
        product_id = product.id
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_qty': product_qty,
                'price': product.price
            }

        # Updates DB w/ cart data
        self.session.modified = True

    def __len__(self):
        return sum(item['product_qty'] for item in self.cart.values())