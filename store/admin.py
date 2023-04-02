from django.contrib import admin

from .models import Category, Product, Color, Material, ProductVariant


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name", "sex",]}


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Material)
