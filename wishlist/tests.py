from django.test import TestCase, Client
from store.models import Material, Category, Product, ProductVariant, Color


class TestUrls(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.material_a = Material.objects.create(
            name='leather'
        )
        cls.material_b = Material.objects.create(
            name='canvas'
        )
        cls.category_a = Category.objects.create(
            name='shoes',
            slug='shoes',
            description='testdescription'
        )
        cls.category_b = Category.objects.create(
            name='boots',
            slug='boots',
            description='testdescription'
        )
        cls.product_a = Product.objects.create(
            name='example one',
            slug='example-one',
            description='example-one description',
            price=129.99,
            sex='Women',
            material=cls.material_a,
            category=cls.category_a
        )
        cls.product_b = Product.objects.create(
            name='product two',
            slug='product-two',
            description='product_b description',
            price=399.99,
            sex='Men',
            material=cls.material_b,
            category=cls.category_b
        )
        cls.color_a = Color.objects.create(
            name='black',
            code='000000'
        )
        cls.color_b = Color.objects.create(
            name='white',
            code='ffffff'
        )
        cls.product_variant_a = ProductVariant.objects.create(
            product=cls.product_a,
            size=39,
            color=cls.color_a,
            available_units=1200,
            sale=True,
            new=True,
            promo=True
        )
        cls.product_variant_b = ProductVariant.objects.create(
            product=cls.product_b,
            size=41,
            color=cls.color_b,
            available_units=1200,
            sale=False,
            new=False,
            promo=False
        )
        cls.product_variant_c = ProductVariant.objects.create(
            product=cls.product_a,
            size=42,
            color=cls.color_b,
            available_units=0,
            sale=True,
            new=False,
            promo=False
        )

    def setUp(self):
        self.c = Client()

    def test_wishlist(self):
        response = self.c.get('/wishlist/')
        self.assertEqual(response.status_code, 200)

    def test_wishlist_modify_get(self):
        response = self.c.get('/wishlist/modify/')
        self.assertEqual(response.status_code, 405)

    def test_wishlist_modify_post_add_correct(self):
        request = {
            'product_id': self.product_a.id,
            'product_size': self.product_variant_a.size,
            'product_color_id': self.product_variant_a.color.id,
            'action': 'add'
        }
        response = self.c.post('/wishlist/modify/', request)
        self.assertEqual(response.status_code, 200)

    def test_wishlist_modify_post_add_404(self):
        request = {
            'product_id': self.product_b.id,
            'product_size': self.product_variant_a.size,
            'product_color_id': self.product_variant_a.color.id,
            'action': 'add'
        }
        response = self.c.post('/wishlist/modify/', request)
        self.assertEqual(response.status_code, 404)

        request = {
            'product_id': self.product_a.id,
            'product_size': self.product_variant_b.size,
            'product_color_id': self.product_variant_a.color.id,
            'action': 'add'
        }
        response = self.c.post('/wishlist/modify/', request)
        self.assertEqual(response.status_code, 404)

        request = {
            'product_id': self.product_a.id,
            'product_size': self.product_variant_a.size,
            'product_color_id': self.product_variant_b.color.id,
            'action': 'add'
        }
        response = self.c.post('/wishlist/modify/', request)
        self.assertEqual(response.status_code, 404)

    def test_wishlist_modify_post_delete_correct(self):
        request = {
            'product_id': self.product_a.id,
            'product_size': self.product_variant_a.size,
            'product_color_id': self.product_variant_a.color.id,
            'action': 'add'
        }
        response = self.c.post('/wishlist/modify/', request)
        self.assertEqual(response.status_code, 200)

        request = {
            'product_id': self.product_a.id,
            'product_size': self.product_variant_a.size,
            'product_color_id': self.product_variant_a.color.id,
            'action': 'delete'
        }
        response = self.c.post('/wishlist/modify/', request)
        self.assertEqual(response.status_code, 200)

    def test_wishlist_modify_post_delete_404(self):
        request = {
            'product_id': self.product_a.id,
            'product_size': self.product_variant_a.size,
            'product_color_id': self.product_variant_a.color.id,
            'action': 'delete'
        }
        response = self.c.post('/wishlist/modify/', request)
        self.assertEqual(response.status_code, 404)
