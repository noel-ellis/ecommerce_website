from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Category, Product


class TestCategoryModel(TestCase):
    def setUp(self):
        self.c = Client()
        self.username = 'admin'
        self.password = 'admin123'
        self.user = User.objects.create_superuser(username=self.username, password=self.password)
        self.category = Category.objects.create(name='testcategory', slug='testcategory')

    def test_category_model_return(self):
        self.assertEqual(str(self.category), 'testcategory')

    def test_category_model_get_abs_url(self):
        self.assertEqual(self.category.get_absolute_url(), reverse("store:category", kwargs={"slug": "testcategory"}))

    """
    Test views
    """
    def test_category_list_view(self):
        response = self.c.get(reverse("store:category", kwargs={"slug": "testcategory"}))
        self.assertEqual(response.status_code, 200)

    def test_category_create_view(self):
        name = 'testing'

        self.c.login(username=self.username, password=self.password)
        response = self.c.post(reverse("store:category-create"), {'name': name, 'slug': name})
        new_category = Category.objects.get(name=name)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(isinstance(new_category, Category))
        self.assertEqual(new_category.name, name)


class TestProductModel(TestCase):
    def setUp(self):
        self.c = Client()
        self.username = 'admin'
        self.password = 'admin123'
        self.user = User.objects.create_superuser(username=self.username, password=self.password)

        self.category = Category.objects.create(name='testcategory', slug='testcategory')
        self.product = Product.objects.create(
            quantity=100,
            price=99,
            name='testproduct',
            description='testdescription',
            category_id=self.category.id,
            slug='testproduct'
        )

    def test_product_model_return(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(str(self.product), 'testproduct')

    def test_product_model_get_abs_url(self):
        self.assertEqual(self.product.get_absolute_url(),
                         reverse("store:product-detail",
                         kwargs={"slug": "testproduct"}))

    """
    Test views
    """
    def test_product_deatil_view(self):
        response = self.c.get(reverse("store:product-detail", kwargs={"slug": "testproduct"}))
        self.assertEqual(response.status_code, 200)

    def test_product_create_view(self):
        name = 'testing_product_view'

        self.c.login(username=self.username, password=self.password)
        response = self.c.post(reverse("store:product-create"),
                               {
                                   'name': name,
                                   'description': 'test_description',
                                   'slug': name,
                                   'price': 100,
                                   'quantity': 99,
                                   'category': self.category.id
                               })
        new_product = Product.objects.get(name=name)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(isinstance(new_product, Product))
        self.assertEqual(new_product.name, name)

    def test_product_update_view(self):
        description = 'test_description_test'

        self.c.login(username=self.username, password=self.password)
        response = self.c.post(reverse("store:product-update", kwargs={"slug": self.product.slug}),
                               {
                                   'name': self.product.name,
                                   'description': description,
                                   'slug': self.product.name,
                                   'price': 100,
                                   'quantity': 99,
                                   'category': self.category.id
                               })
        updated_product = Product.objects.get(name=self.product.name)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(isinstance(updated_product, Product))
        self.assertEqual(updated_product.description, description)

    def test_product_delete_view(self):
        # Not logged in
        response = self.c.get(reverse("store:product-delete", kwargs={"slug": self.product.slug}))
        self.assertEqual(response.status_code, 302)

        # Not admin
        self.user = User.objects.create_user(username='testuser', password='testuser')
        self.c.login(username='testuser', password='testuser')
        response = self.c.get(f'/{self.product.slug}/delete')
        self.assertEqual(response.status_code, 403)

        # Admin
        self.c.login(username=self.username, password=self.password)
        response = self.c.get(f'/{self.product.slug}/delete')
        self.assertEqual(response.status_code, 200)


class TestUrls(TestCase):
    def setUp(self):
        self.c = Client()

    def test_homepage_html(self):
        response = self.c.get('/')
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<a class="navbar-brand mb-0 h1" href="/"><b>WhackShop</b></a>', html)
