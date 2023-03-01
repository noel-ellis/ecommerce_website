from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Collection, Product
from wishlist.wishlist import Wishlist


def main(request):
    return render(request, 'store/main.html')


def collection_list(request, slug):
    collection = get_object_or_404(Collection, slug=slug)
    products = Product.objects.filter(collection=collection)
    return render(request, 'store/collection_list.html', {'collection': collection, 'products': products})


def product_list_view(request):
    wishlist = Wishlist(request)
    wishlist_product_ids = [wishlist_product['product_id'] for wishlist_product in list(wishlist)]
    all_products = Product.objects.all()
    product_list = []
    
    # TESTING
    # =======================================
    print(f'\n\nwishlist_product_ids:\n{wishlist_product_ids}\n')
    print(f'\n1 in wishlist_product_ids:\n{1 in wishlist_product_ids}\n\n')
    # =======================================
    # TESTING

    for product in all_products:
        product_wishlist_mixed = {}
        product_wishlist_mixed['id'] = product.id
        product_wishlist_mixed['image'] = product.image
        product_wishlist_mixed['name'] = product.name
        product_wishlist_mixed['slug'] = product.slug
        product_wishlist_mixed['description'] = product.description
        product_wishlist_mixed['sex'] = product.sex
        product_wishlist_mixed['price'] = str(product.price)
        product_wishlist_mixed['sale'] = product.sale
        product_wishlist_mixed['new'] = product.new
        product_wishlist_mixed['collection'] = product.collection
        product_wishlist_mixed['in_wishlist'] = False
        if product.id in wishlist_product_ids:
            product_wishlist_mixed['in_wishlist'] = True
        product_list.append(product_wishlist_mixed)

    context = {
        'product_list': product_list,
        'is_paginated': False,
    }
    return render(request, 'store/product_list.html', context=context)


class CollectionCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Collection
    fields = ['image', 'name', 'slug', 'description', 'season']

    def test_func(self):
        return self.request.user.has_perm('store.add_collection')


class ProductDetailView(generic.DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'collection', 'quantity', 'image', 'slug']
    fields = [
        'collection',
        'name',
        'slug',
        'description',
        'price',
        'quantity',
        'sex',
        'size',
        'sale',
        'new',
        'image',
    ]


    def test_func(self):
        return self.request.user.has_perm('store.add_product')


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'collection', 'quantity', 'image']

    def test_func(self):
        return self.request.user.has_perm('store.change_product')


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        return self.request.user.has_perm('store.delete_product')
