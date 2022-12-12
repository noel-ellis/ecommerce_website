from django.test import TestCase
from .models import Category, Product
from django.contrib.auth.models import User

class TestCategoryModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='testcategory', slug='testcategory')

    def test_category_model_return(self):
        self.assertEqual(str(self.category), 'testcategory')


class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name='testcategory', slug='testcategory')
        User.objects.create(username='admin')
        self.product = Product.objects.create(
            quantity = 100,
            price = 99,
            name = 'testproduct',
            description = 'testdescription',
            category_id = 2,
            slug = 'testproduct'
        )

    def test_product_model(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(str(self.product), 'testproduct')



