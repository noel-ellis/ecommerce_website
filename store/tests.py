from .models import Category, Product
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

class TestCategoryModel(TestCase):
    def setUp(self):
        self.c = Client()
        self.category = Category.objects.create(name='testcategory', slug='testcategory')

    def test_category_model_return(self):
        self.assertEqual(str(self.category), 'testcategory')

    def test_category_model_url(self):
        response = self.c.get(reverse("store:category", kwargs={"slug": "testcategory"}))
        self.assertEqual(response.status_code, 200)

    def test_category_model_get_abs_url(self):
        self.assertEqual(self.category.get_absolute_url(), reverse("store:category", kwargs={"slug": "testcategory"}))



class TestProductModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='testcategory', slug='testcategory')
        User.objects.create(username='admin')
        self.product = Product.objects.create(
            quantity = 100,
            price = 99,
            name = 'testproduct',
            description = 'testdescription',
            category_id = self.category.id,
            slug = 'testproduct'
        )
        self.c = Client()

    def test_product_model(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(str(self.product), 'testproduct')

    def test_product_model_url(self):
        response = self.c.get(reverse("store:product-detail", kwargs={"slug": "testproduct"}))
        self.assertEqual(response.status_code, 200)

    def test_product_model_get_abs_url(self):
        self.assertEqual(self.product.get_absolute_url(), reverse("store:product-detail", kwargs={"slug": "testproduct"}))


class TestUrls(TestCase):
    def setUp(self):
        self.c = Client()

    def test_homepage_html(self):
        response = self.c.get('/')
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<a class="navbar-brand mb-0 h1" href="/"><b>WhackShop</b></a>', html)




    

