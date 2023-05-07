from django.core.files.storage import default_storage
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views import View

from watson import search as watson

from .models import Category, Product, ProductVariant, Color, Material
from wishlist.wishlist import Wishlist
from ecommerce_website.choices import SIZES_LIST as SIZES


def main(request):
    promo = ProductVariant.objects.filter(promo=True).select_related("product", "product__material")[:4]
    new = ProductVariant.objects.filter(new=True).select_related("product", "product__material")[:4]
    context = {
        "promo": promo,
        "new": new,
    }
    return render(request, "store/main.html", context=context)


class ProductListView(View):
    db_query = ProductVariant.objects.select_related("product__material", "color").values(
        "product__material__name", "product__name", "product__price", "product__slug", "product__id", "color__name", "color__id", "image", "id", "size")
    colors = Color.objects.all()
    materials = Material.objects.all()
    categories = Category.objects.all()

    def search(self, request):
        search_query = request.GET.get("search", "")
        if search_query:
            search_results = watson.search(search_query)
            search_results_ids = [result.object.id for result in search_results]
            self.db_query = self.db_query.filter(product__id__in=search_results_ids)

        return search_query

    def apply_filters(self, request):

        # catching filters
        categories_ids = request.GET.get("categories", "").split(",")
        sizes_ids = request.GET.get("sizes", "").split(",")
        colors_ids = request.GET.get("colors", "").split(",")
        materials_ids = request.GET.get("materials", "").split(",")
        price_cap = request.GET.get("pricecap", "1000")
        select_new = request.GET.get("new", False)
        select_on_sale = request.GET.get("sale", False)
        select_in_stock = request.GET.get("instock", False)

        # applying available filters
        self.db_query = self.db_query.filter(product__price__lte=price_cap)

        if categories_ids != ['']:
            self.db_query = self.db_query.filter(product__category__id__in=categories_ids)
        if sizes_ids != ['']:
            self.db_query = self.db_query.filter(size__in=sizes_ids)
        if colors_ids != ['']:
            self.db_query = self.db_query.filter(color__id__in=colors_ids)
        if materials_ids != ['']:
            self.db_query = self.db_query.filter(product__material__id__in=materials_ids)

        if select_new:
            self.db_query = self.db_query.filter(new=True)
        if select_in_stock:
            self.db_query = self.db_query.filter(available_units__gt=0)
        if select_on_sale:
            self.db_query = self.db_query.filter(sale=True)

    def add_wishlist_data(self, request):
        wishlist = Wishlist(request)
        for product_variant in self.db_query:
            product_variant["in_wishlist"] = wishlist.contains(str(product_variant["id"]))

    def add_images(self):
        for product_variant in self.db_query:
            image_url = default_storage.url(product_variant["image"])
            product_variant["image"] = image_url

    def get_page(self, request):
        paginator = Paginator(self.db_query, 12)
        page_number = request.GET.get('page')
        return paginator.get_page(page_number)

    def get(self, request):
        search_query = self.search(request)
        self.apply_filters(request)
        self.add_wishlist_data(request)
        self.add_images()

        context = {
            "page_obj": self.get_page(request),
            "sizes": SIZES,
            "colors": self.colors,
            "materials": self.materials,
            "categories": self.categories,
            "search_query": search_query,
        }

        return render(request, "store/product_list.html", context=context)


class ProductDetailView(View):

    def get_product(self, slug):
        return Product.objects.get(slug=slug)

    def get_product_variants(self, product):
        return ProductVariant.objects.select_related("color").filter(product=product, available_units__gt=0).values("id", "size", "color__id", "color__code", "color__name", "image")

    def get_wishlist(self, request):
        wishlist = Wishlist(request)
        return wishlist

    def get_promo(self):
        return ProductVariant.objects.filter(promo=True).select_related("product", "product__material")[:3]

    # product_variants_data = {size: [{'id': color_id, 'code': color_code, 'name': color_name, 'in_wishlist': bool'}, ...]}
    # purpose:
    # 1. properly reflect the availability of each color for each size
    # 2. determine if particular ProductVariant is in the user's wishlist
    def get_product_variants_data(self, product, wishlist):
        product_variants = self.get_product_variants(product)

        product_variants_data = {}
        for product_variant in product_variants:
            in_wishlist = wishlist.contains(str(product_variant['id']))
            product_variant_specs = {
                "color_id": product_variant["color__id"],
                "color_code": product_variant["color__code"],
                "color_name": product_variant["color__name"],
                "in_wishlist": str(in_wishlist),
            }
            if product_variant["size"] not in product_variants_data.keys():
                product_variants_data[product_variant["size"]] = []
            product_variants_data[product_variant["size"]].append(product_variant_specs)

        return product_variants_data

    def get_images(self, product):
        product_variants = self.get_product_variants(product)
        product_images = []
        for product_variant in product_variants:
            image_url = default_storage.url(product_variant["image"])
            product_images.append(image_url)

        return product_images

    def get(self, request, slug):
        product = self.get_product(slug)
        wishlist = self.get_wishlist(request)
        product_variants_data = self.get_product_variants_data(product, wishlist)

        context = {
            "product": product,
            "images": self.get_images(product),
            "product_variants_data": product_variants_data,
            "promo": self.get_promo(),
        }

        return render(request, "store/product_detail.html", context=context)
