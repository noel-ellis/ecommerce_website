from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import generic

from .models import Category, Product, Color, Material
from wishlist.wishlist import Wishlist
from ecommerce_website.choices import SIZES_LIST as sizes


def main(request):
    promo = Product.objects.filter(promo=True)[:4]
    new = Product.objects.filter(new=True)[:4]
    context = {
        'promo': promo,
        'new': new,
    }
    return render(request, 'store/main.html', context=context)


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


def product_list_view(request):
    wishlist = Wishlist(request)
    wishlist_product_ids = [wishlist_product['id'] for wishlist_product in list(wishlist)]
    all_products = Product.objects.all()
    colors = Color.objects.all()
    materials = Material.objects.all()
    categories = Category.objects.all()

    product_list = []
    for product in all_products:
        product_wishlist_mixed = {}
        product_wishlist_mixed['id'] = product.id
        product_wishlist_mixed['image'] = product.image
        product_wishlist_mixed['name'] = product.name
        product_wishlist_mixed['slug'] = product.slug
        product_wishlist_mixed['sex'] = product.sex
        product_wishlist_mixed['price'] = str(product.price)
        product_wishlist_mixed['sale'] = product.sale
        product_wishlist_mixed['new'] = product.new
        product_wishlist_mixed['promo'] = product.promo
        product_wishlist_mixed['material'] = product.material.name
        product_wishlist_mixed['color'] = product.color.name
        product_wishlist_mixed['category'] = product.category
        product_wishlist_mixed['in_wishlist'] = False
        if product.id in wishlist_product_ids:
            product_wishlist_mixed['in_wishlist'] = True
        product_list.append(product_wishlist_mixed)

    context = {
        'product_list': product_list,
        'sizes': sizes,
        'colors': colors,
        'materials': materials,
        'categories': categories,
        'is_paginated': False,
    }
    return render(request, 'store/product_list.html', context=context)
    

class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Category
    fields = [
        'image',
        'name',
        'slug',
        'description',
    ]

    def test_func(self):
        return self.request.user.has_perm('store.change_product')


def product_detail_view(request, slug):
    product = Product.objects.filter(slug=slug).first()
    colors = Color.objects.all()
    promo = Product.objects.filter(promo=True)[:3]

    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'promo': promo,
    }
    return render(request, 'store/product_detail.html', context=context)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Product
    fields = [
        'image',
        'name',
        'slug',
        'description',
        'price',
        'quantity',
        'sex',
        'size',
        'color',
        'sale',
        'new',
        'promo',
        'material',
        'category',
    ]

    def test_func(self):
        return self.request.user.has_perm('store.change_product')


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        return self.request.user.has_perm('store.delete_product')
