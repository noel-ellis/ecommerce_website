from store.models import ProductVariant


class Wishlist:
    def __init__(self, request):
        self.__session_wishlist_name = 'wishlist'
        self.__session = request.session

        if self.__session_wishlist_name not in self.__session:
            self.__wishlist = request.session[self.__session_wishlist_name] = {
            }
            return
        self.__wishlist = request.session.get(self.__session_wishlist_name)

    @property
    def __ids(self):
        return list(self.__wishlist)

    def __save(self):
        self.__session.modified = True

    def add(self, product: ProductVariant):
        product_id = str(product.id)
        if product_id not in self.__wishlist:
            self.__wishlist[product_id] = 'data'
            self.__save()
            return

    def delete(self, product: ProductVariant):
        product_id = str(product.id)
        if product_id in self.__wishlist:
            del self.__wishlist[product_id]
            self.__save()
            return
        return 404

    def contains(self, product_id: str):
        return product_id in self.__ids

    def __len__(self):
        return len(self.__wishlist)

    def __str__(self):
        return str(self.__ids)

    def __iter__(self):
        products_from_wishlist = ProductVariant.objects.filter(
            id__in=self.__ids)
        for product in products_from_wishlist:
            product_from_wishlist = {}
            product_from_wishlist['id'] = product.id
            product_from_wishlist['product__id'] = product.product.id
            product_from_wishlist['color__id'] = product.color.id
            product_from_wishlist['size'] = product.size
            product_from_wishlist['name'] = product.product.name
            product_from_wishlist['slug'] = product.product.slug
            product_from_wishlist['material'] = product.product.material
            product_from_wishlist['color'] = product.color.name
            product_from_wishlist['price'] = product.product.price
            product_from_wishlist['image'] = product.image
            yield product_from_wishlist
