from django.db import models

from users.models import UserBase, DeliveryInfo

from store.models import Product


class OrderedItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.product} {self.quantity}x{self.price}'


class Order(models.Model):
    STATUSES = (
        ('ST1', 'status-1'),
        ('ST2', 'status-2'),
        ('ST3', 'status-3'),
        ('ST4', 'status-4'),
    )
    
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    delivery_info = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE)
    ordered_items = models.ManyToManyField(OrderedItem)
    status = models.CharField(max_length=3, choices=STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    

