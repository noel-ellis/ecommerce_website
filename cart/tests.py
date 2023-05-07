from unittest import skip

from importlib import import_module

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.conf import settings

from .cart import Cart
from store.models import Collection, Product


class TestCartViews(TestCase):
    def setUp(self):
        self.c = Client()

    def test_cart_summary_view(self):
        response = self.c.get(reverse('cart:summary'))
        self.assertEqual(response.status_code, 200)

    def test_cart_checkout_view(self):
        response = self.c.get(reverse('cart:checkout'))
        self.assertEqual(response.status_code, 200)


class TestCartEdit(TestCase):
    def setUp(self):
        self.c = Client()
        self.username = 'admin'
        self.password = 'admin123'
        self.user = User.objects.create_superuser(username=self.username, password=self.password)

        self.collection = Collection.objects.create(
            name='testcollection', slug='testcollection', description='description', season='SP')
        self.product = Product.objects.create(
            name='testproduct',
            slug='testproduct',
            description='testdescription',
            quantity=100,
            price=99,
            collection_id=self.collection.id,
            sex='M',
            size='43'
        )

    def test_cart_add(self):
        response = self.c.post(reverse('cart:modify'), {
            'product_id': '1',
            'product_qty': '3',
            'action': 'add'
        }, xhr=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['qty'], 3)

    def test_cart_update(self):
        self.c.post(reverse('cart:modify'), {
            'product_id': '3',
            'product_qty': '1',
            'action': 'add'
        }, xhr=True)

        response = self.c.post(reverse('cart:modify'), {
            'product_id': '3',
            'product_qty': '10',
            'action': 'update'
        }, xhr=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['qty'], 10)
        self.assertEqual(response.json()['totalqty'], 10)
        self.assertEqual(response.json()['totalprice'], '990.00')
        self.assertEqual(response.json()['subtotalprice'], '990.00')

    def test_cart_delete(self):
        self.c.post(reverse('cart:modify'), {
            'product_id': '2',
            'product_qty': '1',
            'action': 'add'
        }, xhr=True)

        response = self.c.post(reverse('cart:modify'), {
            'product_id': '2',
            'action': 'delete'
        }, xhr=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['totalqty'], 0)
        self.assertEqual(response.json()['totalprice'], 0)


class TestCartFunctions(TestCase):
    def setUp(self):
        self.c = Client()
        self.username = 'admin'
        self.password = 'admin123'
        self.user = User.objects.create_superuser(username=self.username, password=self.password)

        self.collection = Collection.objects.create(
            name='testcollection', slug='testcollection', description='description', season='SP')
        self.product = Product.objects.create(
            name='testproduct',
            slug='testproduct',
            description='testdescription',
            quantity=100,
            price=99,
            collection_id=self.collection.id,
            sex='M',
            size='43'
        )

    @skip('not ready yet')
    def test_cart_save(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        cart = Cart(request)
        self.assertEqual(cart.total, 0)
        product = Product.objects.first()
        cart.add(product=product, product_qty=1)
        self.assertEqual(cart.total, 1)
