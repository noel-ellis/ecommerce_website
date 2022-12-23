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
