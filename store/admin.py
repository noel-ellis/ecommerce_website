from django.contrib import admin

from .models import Category, Product, Color, Material

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Material)
