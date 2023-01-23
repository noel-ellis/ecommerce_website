from django.db import models
from django.urls import reverse


class Collection(models.Model):
    SEASONS = (
        ('WI', 'Winter'),
        ('SP', 'Spring'),
        ('SU', 'Summer'),
        ('FA', 'Fall'),
    )
    image = models.ImageField(blank=True, default='default_collection.png', upload_to='collection_pics')
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    season = models.CharField(max_length=2, choices=SEASONS)

    class Meta:
        verbose_name_plural = 'Collections'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:collection", kwargs={"slug": self.slug})


class Product(models.Model):
    image = models.ImageField(blank=True, default='default_item.png', upload_to='product_pics')
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("store:product-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-date_modified',)

    def __str__(self):
        return self.name
