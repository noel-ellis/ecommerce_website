from django.db import models
from django.urls import reverse
from ecommerce_website.choices import SEXES, SIZES


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:categories")

    class Meta:
        verbose_name_plural = 'Categories'


class Color(models.Model):
    name = models.CharField(max_length=25, unique=True)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    sex = models.CharField(max_length=5, choices=SEXES)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("store:product-detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ('-date_modified',)
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, default='/product_pics/default_item.png', upload_to='product_pics')
    size = models.CharField(max_length=4, choices=SIZES)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    available_units = models.PositiveIntegerField()
    sale = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    promo = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product.name}; {self.color}, {self.size}'

    class Meta:
        verbose_name_plural = 'Product Variants'
