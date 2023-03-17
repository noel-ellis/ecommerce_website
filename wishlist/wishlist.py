from store.models import Product


class Wishlist:
    def __init__(self, request):
        self.session_wishlist_name = 'wishlist'
        self.session = request.session

        if self.session_wishlist_name not in self.session:
            self.wishlist = request.session[self.session_wishlist_name] = {}
            return 
        self.wishlist = request.session.get(self.session_wishlist_name)

    def save(self):
        self.session.modified = True

    def add(self, product: Product):
        product_id = str(product.id)
        if product_id not in self.wishlist:
            self.wishlist[product_id] = 'data'
            self.save()
            return

    def delete(self, product: Product):
        product_id = str(product.id)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()
            return

    def __len__(self):
        return len(self.wishlist)
    
    def __str__(self):
        return f'{list(self.wishlist.keys())}'
    
    def __iter__(self):
        product_ids = self.wishlist.keys()
        products_from_wishlist = Product.objects.filter(id__in=product_ids)
        for product in products_from_wishlist:
            product_from_wishlist = {}
            product_from_wishlist['id'] = product.id
            product_from_wishlist['name'] = product.name
            product_from_wishlist['slug'] = product.slug
            product_from_wishlist['material'] = product.material
            product_from_wishlist['color'] = product.color
            product_from_wishlist['price'] = product.price
            product_from_wishlist['image'] = product.image
            yield product_from_wishlist
