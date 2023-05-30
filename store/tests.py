from django.test import Client, TestCase

from decimal import Decimal

from .models import Material, Category, Product, Color, ProductVariant
from ecommerce_website.choices import SIZES_LIST as SIZES


class TestProductListView(TestCase):
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

    def test_store(self):
        response = self.c.get('/store')
        self.assertEqual(response.context['colors'][0], self.color_a)
        self.assertEqual(response.context['colors'][1], self.color_b)
        self.assertEqual(response.context['materials'][0], self.material_a)
        self.assertEqual(response.context['materials'][1], self.material_b)
        self.assertEqual(response.context['categories'][0], self.category_a)
        self.assertEqual(response.context['categories'][1], self.category_b)
        self.assertEqual(response.context['sizes'], SIZES)
        self.assertEqual(response.context['search_query'], '')
        self.assertEqual(response.context['page_obj'].number, 1)

        self.assertEqual(response.context['page_obj'].object_list[0]['product__material__name'], self.material_a.name)
        self.assertEqual(response.context['page_obj'].object_list[0]['product__name'], self.product_a.name)
        self.assertEqual(response.context['page_obj'].object_list[0]['product__price'], Decimal('129.99'))
        self.assertEqual(response.context['page_obj'].object_list[0]['product__slug'], self.product_a.slug)
        self.assertEqual(response.context['page_obj'].object_list[0]['product__id'], self.product_a.id)
        self.assertEqual(response.context['page_obj'].object_list[0]['color__name'], self.color_a.name)
        self.assertEqual(response.context['page_obj'].object_list[0]['color__id'], self.color_a.id)
        self.assertEqual(response.context['page_obj'].object_list[0]['image'], '/media/product_pics/default_item.png')
        self.assertEqual(response.context['page_obj'].object_list[0]['id'], self.product_variant_a.id)
        self.assertEqual(response.context['page_obj'].object_list[0]['size'], str(self.product_variant_a.size))
        self.assertEqual(response.context['page_obj'].object_list[0]['in_wishlist'], False)

    def test_filters(self):
        # category
        response = self.c.get('/store?categories=1')
        self.assertEqual(len(response.context['page_obj'].object_list), 2)

        # size
        response = self.c.get('/store?sizes=39')
        self.assertEqual(len(response.context['page_obj'].object_list), 1)
        self.assertEqual(response.context['page_obj'].object_list[0]['size'], '39')

        response = self.c.get('/store?sizes=41')
        self.assertEqual(len(response.context['page_obj'].object_list), 1)
        self.assertEqual(response.context['page_obj'].object_list[0]['size'], '41')

        response = self.c.get('/store?sizes=42')
        self.assertEqual(len(response.context['page_obj'].object_list), 1)
        self.assertEqual(response.context['page_obj'].object_list[0]['size'], '42')

        response = self.c.get('/store?sizes=39%2C41%2C42')
        self.assertEqual(len(response.context['page_obj'].object_list), 3)
        self.assertEqual(response.context['page_obj'].object_list[0]['size'], '39')
        self.assertEqual(response.context['page_obj'].object_list[1]['size'], '41')
        self.assertEqual(response.context['page_obj'].object_list[2]['size'], '42')

        # color
        response = self.c.get('/store?colors=2')
        self.assertEqual(len(response.context['page_obj'].object_list), 2)
        self.assertEqual(response.context['page_obj'].object_list[0]['color__id'], 2)
        self.assertEqual(response.context['page_obj'].object_list[1]['color__id'], 2)
        response = self.c.get('/store?colors=1')
        self.assertEqual(len(response.context['page_obj'].object_list), 1)
        self.assertEqual(response.context['page_obj'].object_list[0]['color__id'], 1)

        # material
        response = self.c.get('/store?materials=2')
        self.assertEqual(len(response.context['page_obj'].object_list), 1)
        self.assertEqual(response.context['page_obj'].object_list[0]['product__material__name'], 'canvas')
        response = self.c.get('/store?materials=1')
        self.assertEqual(len(response.context['page_obj'].object_list), 2)
        self.assertEqual(response.context['page_obj'].object_list[0]['product__material__name'], 'leather')
        self.assertEqual(response.context['page_obj'].object_list[1]['product__material__name'], 'leather')

        # price cap
        response = self.c.get('/store?pricecap=300')
        self.assertEqual(len(response.context['page_obj'].object_list), 2)
        response = self.c.get('/store?pricecap=400')
        self.assertEqual(len(response.context['page_obj'].object_list), 3)
        response = self.c.get('/store?pricecap=100')
        self.assertEqual(len(response.context['page_obj'].object_list), 0)

        # new
        response = self.c.get('/store?new=true')
        self.assertEqual(len(response.context['page_obj'].object_list), 1)

        # sale
        response = self.c.get('/store?sale=true')
        self.assertEqual(len(response.context['page_obj'].object_list), 2)

        # in stock
        response = self.c.get('/store?instock=true')
        self.assertEqual(len(response.context['page_obj'].object_list), 2)

    def test_search(self):
        response = self.c.get('/store?search=example')
        self.assertEqual(len(response.context['page_obj'].object_list), 2)
        response = self.c.get('/store?search=loremipsum')
        self.assertEqual(len(response.context['page_obj'].object_list), 0)


class TestProductDetailsView(TestCase):
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
            product=cls.product_a,
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
        cls.product_variant_d = ProductVariant.objects.create(
            product=cls.product_a,
            size=39,
            color=cls.color_b,
            available_units=1200,
            sale=True,
            new=True,
            promo=True
        )

    def setUp(self):
        self.c = Client()

    def test_product(self):
        response = self.c.get('/store/example-one')
        self.assertEqual(response.context['product'], self.product_a)

    def test_images(self):
        response = self.c.get('/store/example-one')
        self.assertEqual(len(response.context['images']), 3)
        self.assertEqual(response.context['images'][0], '/media/product_pics/default_item.png')
        self.assertEqual(response.context['images'][1], '/media/product_pics/default_item.png')
        self.assertEqual(response.context['images'][2], '/media/product_pics/default_item.png')

    def test_product_variants_data(self):
        response = self.c.get('/store/example-one')
        self.assertEqual(len(response.context['product_variants_data']), 2)
        self.assertIn('39', response.context['product_variants_data'])
        self.assertIn('41', response.context['product_variants_data'])
        self.assertEqual(len(response.context['product_variants_data']['39']), 2)
        self.assertEqual(response.context['product_variants_data']['39']
                         [0]['color_id'], self.product_variant_a.color.id)
        self.assertEqual(response.context['product_variants_data']['39']
                         [1]['color_id'], self.product_variant_d.color.id)
        self.assertEqual(response.context['product_variants_data']['41']
                         [0]['color_id'], self.product_variant_b.color.id)

    def test_promo(self):
        response = self.c.get('/store/example-one')
        print(f"\nRESPONSE.CONTEXT:\n{response.context['promo']}\n")
        self.assertEqual(len(response.context['promo']), 2)


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
