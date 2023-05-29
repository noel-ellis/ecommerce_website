from django.test import Client, TestCase


class TestProductListView(TestCase):
    def setUp(self):
        pass


class TestUrls(TestCase):
    def setUp(self):
        self.c = Client()

    def test_homepage(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_store(self):
        response = self.c.get('/store')
        self.assertEqual(response.status_code, 200)
