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
    for product in all_products:
        product["in_wishlist"] = wishlist.contains(str(product["id"]))
        image_url = default_storage.url(product["image"])
        product["image"] = image_url  

    context = {
        "product_list": all_products,
        "sizes": sizes,
        "colors": colors,
        "materials": materials,
        "categories": categories
    }
    return render(request, "store/product_list.html", context=context)


def product_detail_view(request, slug):
    product = Product.objects.get(slug=slug)
    product_variants = ProductVariant.objects.select_related("color").filter(product=product, available_units__gt=0).values("size", "color__id", "color__code", "color__name", "image")

    size_color_pairs = {}
    images = []

    for product_variant in product_variants:
        color_data = {"id": product_variant["color__id"], "code": product_variant["color__code"], "name": product_variant["color__name"],}
        if product_variant["size"] not in size_color_pairs.keys():
            size_color_pairs[product_variant["size"]] = []
        size_color_pairs[product_variant["size"]].append(color_data)

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
