from django.db import models
from django.urls import reverse
from ecommerce_website.choices import SEXES, SIZES


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(blank=True, default='default_item.png', upload_to='category_pics')
    description = models.TextField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("store:categories")
    
    class Meta:
        verbose_name_plural = 'Categories'
    

class Color(models.Model):
    name = models.CharField(max_length=25, unique=True)
    image = models.ImageField(upload_to='color_pics')

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(blank=True, default='default_item.png', upload_to='product_pics')
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    sex = models.CharField(max_length=2, choices=SEXES)
    size = models.CharField(max_length=4, choices=SIZES)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    sale = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    promo = models.BooleanField(default=False)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("store:product-detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ('-date_modified',)

    def __str__(self):
        return self.name
