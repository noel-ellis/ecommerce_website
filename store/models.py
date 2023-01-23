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
    SEXES = (
        ('W', 'Women'),
        ('M', 'Men'),
    )
    SIZES = (
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
        ('45.5', '45.5'),
        ('46', '46'),
        ('47', '47'),
        ('48', '48'),
        ('49', '49'),
        ('50', '50'),
    )
    image = models.ImageField(blank=True, default='default_item.png', upload_to='product_pics')
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    sex = models.CharField(max_length=2, choices=SEXES)
    size = models.CharField(max_length=4, choices=SIZES)
    sale = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("store:product-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-date_modified',)

    def __str__(self):
        return self.name
