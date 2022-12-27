from store.models import Product


class Cart:
    """
    Base Cart Class
    """

    def __init__(self, request):
        self.session = request.session
        if 'skey' not in request.session:
            self.cart = self.session['skey'] = {}
            return
        self.cart = self.session.get('skey')

    def add(self, product: Product):
        print('!!!WORKS!!!')
        product_id = product.id
        if product_id not in self.cart:
            self.cart[product_id] = {
                'price': product.price
            }

        self.session.modified = True
