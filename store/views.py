from django.core.files.storage import default_storage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import generic

from .models import Category, Product, ProductVariant, Color, Material
from wishlist.wishlist import Wishlist
from ecommerce_website.choices import SIZES_LIST as sizes


def main(request):
    promo = ProductVariant.objects.filter(promo=True).select_related("product", "product__material")[:4]
    new = ProductVariant.objects.filter(new=True).select_related("product", "product__material")[:4]
    context = {
        "promo": promo,
        "new": new,
    }
    return render(request, "store/main.html", context=context)


def product_list_view(request):
    wishlist = Wishlist(request)
    colors = Color.objects.all()
    materials = Material.objects.all()
    categories = Category.objects.all()

    all_products = ProductVariant.objects.select_related("product__material", "color").values("product__material__name", "product__name", "product__price", "product__slug", "product__id", "color__name", "color__id", "image", "id", "size").all()
    for product_variant in all_products:
        product_variant["in_wishlist"] = wishlist.contains(str(product_variant["id"]))
        image_url = default_storage.url(product_variant["image"])
        product_variant["image"] = image_url  

    context = {
        "product_list": all_products,
        "sizes": sizes,
        "colors": colors,
        "materials": materials,
        "categories": categories
    }
    return render(request, "store/product_list.html", context=context)


def product_detail_view(request, slug):
    wishlist = Wishlist(request)
    product = Product.objects.get(slug=slug)
    product_variants = ProductVariant.objects.select_related("color").filter(product=product, available_units__gt=0).values("id", "size", "color__id", "color__code", "color__name", "image")

    size_color_pairs = {}
    images = []

    for product_variant in product_variants:
        # creating size-color pairs to: 
        # 1. properly reflect the availability of each color for each size
        # 2. determine whether or not the user added ProductVariant with that color to the wishlist
        # format: 
        # size_color_pairs = {size: [{'id': color_id, 'code': color_code, 'name': color_name, 'in_wishlist': bool'}, ...]}
        in_wishlist = wishlist.contains(str(product_variant['id']))
        product_variant_specs = {
            "color_id": product_variant["color__id"], 
            "color_code": product_variant["color__code"], 
            "color_name": product_variant["color__name"],
            "in_wishlist": str(in_wishlist),
        }
        if product_variant["size"] not in size_color_pairs.keys():
            size_color_pairs[product_variant["size"]] = []
        size_color_pairs[product_variant["size"]].append(product_variant_specs)

        # creating list of images to display on product detail page
        image_url = default_storage.url(product_variant["image"])
        images.append(image_url)

    promo = ProductVariant.objects.filter(promo=True).select_related("product", "product__material")[:3]
    context = {
        "product": product,
        "images": images,
        "size_color_pairs": size_color_pairs,
        "promo": promo,
    }
    return render(request, "store/product_detail.html", context=context)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Product
    fields = [
        "image",
        "name",
        "slug",
        "description",
        "price",
        "quantity",
        "sex",
        "size",
        "color",
        "sale",
        "new",
        "promo",
        "material",
        "category",
    ]

    def test_func(self):
        return self.request.user.has_perm("store.change_product")


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Product
    success_url = "/"

    def test_func(self):
        return self.request.user.has_perm("store.delete_product")
