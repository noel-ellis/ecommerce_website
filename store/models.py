from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:category", kwargs={"slug": self.slug})


class Product(models.Model):
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, default='default_item.png', upload_to='product_pics')
    slug = models.SlugField(max_length=255, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("store:product-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-date_modified',)

    def __str__(self):
        return self.name


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
