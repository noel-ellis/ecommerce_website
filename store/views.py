from django.core.files.storage import default_storage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import generic

from .models import Category, Product, ProductVariant, Color, Material
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


def product_list_view(request):
    wishlist = Wishlist(request)
    colors = Color.objects.all()
    materials = Material.objects.all()
    categories = Category.objects.all()

    all_products = ProductVariant.objects.select_related('product__material', 'color').values("product__material__name", "product__name", "product__price", "product__slug", "product__id", "color__name", "image").all()
    for product in all_products:
        product['in_wishlist'] = wishlist.contains(product['product__id'])
        image_url = default_storage.url(product['image'])
        product['image'] = image_url
        print(f'\n\n===================\nproduct #:\n{product["image"]}\n===================\n\n')

    context = {
        'product_list': all_products,
        'sizes': sizes,
        'colors': colors,
        'materials': materials,
        'categories': categories
    }
    return render(request, 'store/product_list.html', context=context)


def product_detail_view(request, slug):
    product = Product.objects.filter(slug=slug).first()
    product_variants = ProductVariant.objects.select_related('color').filter(product=product)
    colors = []
    sizes = []
    for product_variant in product_variants:
        colors.append(product_variant.color)
        sizes.append(product_variant.size)
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
