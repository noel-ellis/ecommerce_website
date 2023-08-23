import json

from django.test import Client, TestCase
from django.urls import reverse

from store.models import Material, Category, Product, Color, ProductVariant


class TestModifyCartView(TestCase):
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
            slug='shoes'
        )
        cls.category_b = Category.objects.create(
            name='boots',
            slug='boots'
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
            new=True,
            promo=False
        )
        cls.product_variant_c = ProductVariant.objects.create(
            product=cls.product_b,
            size=42,
            color=cls.color_b,
            available_units=0,
            sale=True,
            new=True,
            promo=False
        )
        cls.product_variant_d = ProductVariant.objects.create(
            product=cls.product_b,
            size=39,
            color=cls.color_b,
            available_units=1200,
            sale=True,
            new=False,
            promo=True
        )

    def setUp(self):
        self.c = Client()

    def test_add_valid(self):
        qty = 3, 1
        size = self.product_variant_a.size, self.product_variant_d.size
        color_id = self.product_variant_a.color.id, self.product_variant_d.color.id
        product_id = self.product_variant_a.product.id, self.product_variant_d.product.id

        # add first item
        response = self.c.post(reverse('cart:modify'), {
                               'action': 'add', 'product_id': product_id[0], 'product_size': size[0], 'product_color_id': color_id[0], 'product_qty': qty[0]})
        self.assertEqual(response.status_code, 200)
        context_data = json.loads(response.content)
        self.assertEqual(context_data['qty'], qty[0])
        self.assertEqual(context_data['product_variant_id'], self.product_variant_a.id)
        self.assertEqual(context_data['totalqty'], qty[0])
        self.assertEqual(context_data['totalprice'], f"{(self.product_a.price*qty[0]):.2f}")
        self.assertEqual(context_data['img_url'], self.product_variant_a.image.url)
        self.assertEqual(context_data['size'], str(size[0]))
        self.assertEqual(context_data['color_name'], self.product_variant_a.color.name)

        # add second item
        response = self.c.post(reverse('cart:modify'), {
                               'action': 'add', 'product_id': product_id[1], 'product_size': size[1], 'product_color_id': color_id[1], 'product_qty': qty[1]})
        self.assertEqual(response.status_code, 200)
        context_data = json.loads(response.content)
        self.assertEqual(context_data['qty'], qty[1])
        self.assertEqual(context_data['product_variant_id'], self.product_variant_d.id)
        self.assertEqual(context_data['totalqty'], qty[0]+qty[1])
        self.assertEqual(context_data['totalprice'],
                         f"{(self.product_a.price*qty[0] + self.product_b.price*qty[1]):.2f}")
        self.assertEqual(context_data['img_url'], self.product_variant_d.image.url)
        self.assertEqual(context_data['size'], str(size[1]))
        self.assertEqual(context_data['color_name'], self.product_variant_d.color.name)

    def test_add_invalid_product(self):
        qty = 4
        size = self.product_variant_c.size
        color_id = self.product_variant_a.color.id
        product_id = self.product_variant_c.product.id,
        response = self.c.post(reverse('cart:modify'), {
                               'action': 'add', 'product_id': product_id, 'product_size': size, 'product_color_id': color_id, 'product_qty': qty})
        self.assertEqual(response.status_code, 404)

    def test_add_invalid_qty(self):
        qty = 4
        size = self.product_variant_c.size
        color_id = self.product_variant_c.color.id
        product_id = self.product_variant_c.product.id,
        response = self.c.post(reverse('cart:modify'), {
                               'action': 'add', 'product_id': product_id, 'product_size': size, 'product_color_id': color_id, 'product_qty': qty})
        self.assertEqual(response.status_code, 404)

    def test_delete_valid(self):
        qty = 3, 1
        size = self.product_variant_a.size, self.product_variant_d.size
        color_id = self.product_variant_a.color.id, self.product_variant_d.color.id
        product_id = self.product_variant_a.product.id, self.product_variant_d.product.id

        # add first item
        response = self.c.post(reverse('cart:modify'), {
                               'action': 'add', 'product_id': product_id[0], 'product_size': size[0], 'product_color_id': color_id[0], 'product_qty': qty[0]})
        self.assertEqual(response.status_code, 200)

        # add second item
        response = self.c.post(reverse('cart:modify'), {
                               'action': 'add', 'product_id': product_id[1], 'product_size': size[1], 'product_color_id': color_id[1], 'product_qty': qty[1]})
        self.assertEqual(response.status_code, 200)

        # delete first item
        response = self.c.post(reverse('cart:modify'), {
                               'action': 'delete', 'product_id': product_id[0], 'product_size': size[0], 'product_color_id': color_id[0]})
        self.assertEqual(response.status_code, 200)
        context_data = json.loads(response.content)
        self.assertEqual(context_data['product_variant_id'], self.product_variant_a.id)
        self.assertEqual(context_data['totalqty'], qty[1])
        self.assertEqual(context_data['totalprice'], f"{(self.product_b.price*qty[1]):.2f}")

    # the view allows requests for deleting items that exist in the database, but aren't in the cart. Such requests are ignored.
    def test_delete_invalid_product(self):
        size = self.product_variant_a.size
        color_id = self.product_variant_c.color.id
        product_id = self.product_variant_a.product.id

        response = self.c.post(reverse('cart:modify'), {
                               'action': 'delete', 'product_id': product_id, 'product_size': size, 'product_color_id': color_id})
        self.assertEqual(response.status_code, 404)

    def test_update_valid(self):
        qty = 3, 1, 20
        size = self.product_variant_a.size, self.product_variant_d.size
        color_id = self.product_variant_a.color.id, self.product_variant_d.color.id
        product_id = self.product_variant_a.product.id, self.product_variant_d.product.id

        # add first item
        response = self.c.post(reverse('cart:modify'), {
                               'action': 'add', 'product_id': product_id[0], 'product_size': size[0], 'product_color_id': color_id[0], 'product_qty': qty[0]})
        self.assertEqual(response.status_code, 200)

        # add second item
        response = self.c.post(reverse('cart:modify'), {
                               'action': 'add', 'product_id': product_id[1], 'product_size': size[1], 'product_color_id': color_id[1], 'product_qty': qty[1]})
        self.assertEqual(response.status_code, 200)

        # update second item
        response = self.c.post(reverse('cart:modify'), {
                               'action': 'update', 'product_id': product_id[1], 'product_size': size[1], 'product_color_id': color_id[1], 'product_qty': qty[2]})
        self.assertEqual(response.status_code, 200)
        context_data = json.loads(response.content)
        self.assertEqual(context_data['qty'], qty[2])
        self.assertEqual(context_data['totalqty'], qty[0]+qty[2])
        self.assertEqual(
            context_data['totalprice'], f"{(self.product_variant_a.product.price*qty[0] + self.product_variant_d.product.price*qty[2]):.2f}")
        self.assertEqual(context_data['subtotalprice'], f"{(self.product_variant_d.product.price*qty[2]):.2f}")

    # the view allows requests for updating items that exist in the database, but aren't in the cart. Such requests are ignored.
    def test_update_invalid_product(self):
        qty = 3
        size = self.product_variant_a.size
        color_id = self.product_variant_b.color.id
        product_id = self.product_variant_a.product.id

        response = self.c.post(reverse('cart:modify'), {
                               'action': 'update', 'product_id': product_id, 'product_size': size, 'product_color_id': color_id, 'product_qty': qty})
        self.assertEqual(response.status_code, 404)

    def test_update_invalid_qty(self):
        qty = self.product_variant_a.available_units + 1
        size = self.product_variant_a.size
        color_id = self.product_variant_a.color.id
        product_id = self.product_variant_a.product.id

        response = self.c.post(reverse('cart:modify'), {
                               'action': 'update', 'product_id': product_id, 'product_size': size, 'product_color_id': color_id, 'product_qty': qty})
        self.assertEqual(response.status_code, 404)
