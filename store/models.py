from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Stock(models.Model):
    CATEGORY_A = 'CA'
    CATEGORY_B = 'CB'
    CATEGORY_C = 'CC'
    CATEGORY_CHOICES = [
        (CATEGORY_A, 'Category A'),
        (CATEGORY_B, 'Category B'),
        (CATEGORY_C, 'Category C'),
    ]

    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_A,
        )
    image = models.ImageField(blank=True, default='default_item.png' , upload_to='stock_pics')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('store:stock-detail', kwargs={'pk': self.pk})


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
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=STATUS_IN_CART
    )
