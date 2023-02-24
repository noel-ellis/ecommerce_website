from django.contrib import admin
from .models import Order, OrderedItem

admin.site.register(Order)
admin.site.register(OrderedItem)
