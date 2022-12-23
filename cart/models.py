from django.db import models
from store.models import Product
from django.contrib.auth.models import User


class Cart(models.Model):
    STATUS_IN_CART = 'IC'
    STATUS_ACCEPTED = 'AC'
    STATUS_PROCESSED = 'PR'
    STATUS_SENT = 'SE'
    STATUS_READY = 'RE'
    STATUS_DELIVERED = 'DE'
    STATUS_CHOICES = [
        (STATUS_IN_CART, 'waiting for confirmation'),
        (STATUS_ACCEPTED, 'accepted'),
        (STATUS_PROCESSED, 'processing'),
        (STATUS_SENT, 'sent'),
        (STATUS_READY, 'waiting for delivery'),
        (STATUS_DELIVERED, 'successfully delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=STATUS_IN_CART
    )
