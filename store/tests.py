from django.test import Client, TestCase

from .models import Material, Category, Product, Color, ProductVariant


class TestProductListView(TestCase):
    def setUp(self):
        self.c = Client()
        self.material = Material.objects.create(
            name='leather'
        )
        self.category = Category.objects.create(
            name='shoes',
            slug='shoes',
            description='testdescription'
        )
        self.product = Product.objects.create(
            name='product_a',
            slug='product_a',
            description='product_a description',
            price=129.99,
            sex='Women',
            material=self.material,
            category=self.category
        )
        self.color = Color.objects.create(
            name='black',
            code='000000'
        )
        self.product_variant = ProductVariant.objects.create(
            product=self.product,
            size=39,
            color=self.color,
            available_units=1200,
            sale=True,
            new=True,
            promo=True
        )


class TestUrls(TestCase):
    def setUp(self):
        self.c = Client()
        self.material = Material.objects.create(
            name='leather'
        )
        self.category = Category.objects.create(
            name='shoes',
            slug='shoes',
            description='testdescription'
        )
        self.product = Product.objects.create(
            name='product_a',
            slug='product_a',
            description='product_a description',
            price=129.99,
            sex='Women',
            material=self.material,
            category=self.category
        )

    def test_homepage(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_store(self):
        response = self.c.get('/store')
        self.assertEqual(response.status_code, 200)

    def test_product_details(self):
        response = self.c.get('/store/product_a')
        self.assertEqual(response.status_code, 200)
