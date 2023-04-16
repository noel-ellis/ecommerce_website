from store.models import ProductVariant


class Wishlist:
    def __init__(self, request):
        self.session_wishlist_name = 'wishlist'
        self.session = request.session

        if self.session_wishlist_name not in self.session:
            self.wishlist = request.session[self.session_wishlist_name] = {}
            return 
        self.wishlist = request.session.get(self.session_wishlist_name)

    @property
    def ids(self):
        return list(self.wishlist)
    
    def save(self):
        self.session.modified = True

    def add(self, product: ProductVariant):
        product_id = str(product.id)
        if product_id not in self.wishlist:
            self.wishlist[product_id] = 'data'
            self.save()
            return

    def delete(self, product: ProductVariant):
        product_id = str(product.id)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()
            return
        
    def contains(self, product_id: str):
        return product_id in self.ids

    def __len__(self):
        return len(self.wishlist)
    
    def __str__(self):
        return str(self.ids)
    
    def __iter__(self):
        products_from_wishlist = ProductVariant.objects.filter(id__in=self.ids)
        for product in products_from_wishlist:
            product_from_wishlist = {}
            product_from_wishlist['id'] = product.id
            product_from_wishlist['product__id'] = product.product.id
            product_from_wishlist['color__id'] = product.color.id
            product_from_wishlist['size'] = product.size
            product_from_wishlist['name'] = product.product.name
            product_from_wishlist['slug'] = product.product.slug
            product_from_wishlist['material'] = product.product.material
            product_from_wishlist['price'] = product.product.price
            product_from_wishlist['image'] = product.image
            yield product_from_wishlist
