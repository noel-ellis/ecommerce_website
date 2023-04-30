from django.core.files.storage import default_storage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator

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

# TODO:
# search
def product_list_view(request):
    wishlist = Wishlist(request)
    colors = Color.objects.all()
    materials = Material.objects.all()
    categories = Category.objects.all()

    # catching filters
    categories_ids = request.GET.get("categories", "").split(",")
    sizes_ids = request.GET.get("sizes", "").split(",")
    colors_ids = request.GET.get("colors", "").split(",")
    materials_ids = request.GET.get("materials", "").split(",")
    price_cap = request.GET.get("pricecap", "1000")
    select_new = request.GET.get("new", False)
    select_on_sale = request.GET.get("sale", False)
    select_in_stock = request.GET.get("instock", False)

    # TESTING outputs
    print(f'\n!!!!!!!!\n category ids: {categories_ids}\n size ids: {sizes_ids}\n color ids: {colors_ids}\n material ids: {materials_ids}\n price cap: {price_cap}\n select new: {select_new}\n select in stock: {select_in_stock}\n select on sale: {select_on_sale}\n!!!!!!!!\n')

    # I'll be modifying this query according to filters recieved from the frontend
    all_products = ProductVariant.objects.select_related("product__material", "color").values("product__material__name", "product__name", "product__price", "product__slug", "product__id", "color__name", "color__id", "image", "id", "size").all()
    
    # apply available filters
    all_products = all_products.filter(product__price__lte=price_cap)
    
    if categories_ids != ['']:
        all_products = all_products.filter(product__category__id__in=categories_ids)
    if sizes_ids != ['']:
        all_products = all_products.filter(size__in=sizes_ids)
    if colors_ids != ['']:
        all_products = all_products.filter(color__id__in=colors_ids)
    if materials_ids != ['']:
        all_products = all_products.filter(product__material__id__in=materials_ids)

    if select_new:
        all_products = all_products.filter(new=True)
    if select_in_stock:
        all_products = all_products.filter(available_units__gt=0)
    if select_on_sale:
        all_products = all_products.filter(sale=True)

    # mix-in in_wishlist to each product variant, so that we can properly reflect the availability of each color for each size
    for product_variant in all_products:
        product_variant["in_wishlist"] = wishlist.contains(str(product_variant["id"]))
        image_url = default_storage.url(product_variant["image"])
        product_variant["image"] = image_url

    # pagination
    paginator = Paginator(all_products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
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
