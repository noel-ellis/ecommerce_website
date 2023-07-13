from django.test import Client, TestCase

from .models import UserBase, DeliveryInfo


class TestUrls(TestCase):

    def setUp(self):
        self.c = Client()

    @classmethod
    def setUpTestData(cls):
        cls.user_email = 'test@test.com'
        cls.user_pwd = '123'
        cls.user = UserBase.objects.create_user(
            email = cls.user_email,
            password = cls.user_pwd,
            is_active = True
        )
        cls.address = DeliveryInfo(
            user = cls.user,
            country = DeliveryInfo.COUNTRIES[0][0],
            state = DeliveryInfo.STATES[0][0],
            zip = '0000',
            address = 'test_address'
        )
        cls.address.save()

    def test_settings(self):
        response = self.c.get('/settings/')
        self.assertEqual(response.status_code, 302)

        loggedin = self.c.login(email=self.user_email, password = self.user_pwd)
        self.assertTrue(loggedin)

        response = self.c.get('/settings/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.c.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.c.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_pwd_reset(self):
        response = self.c.get('/password-reset/')
        self.assertEqual(response.status_code, 200)

    def test_pwd_reset_complete(self):
        response = self.c.get('/password-reset-complete/')
        self.assertEqual(response.status_code, 200)

    def test_pwd_reset_done(self):
        response = self.c.get('/password-reset/done/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.c.get('/logout/')
        self.assertEqual(response.status_code, 302)

        loggedin = self.c.login(email=self.user_email, password = self.user_pwd)
        self.assertTrue(loggedin)

        response = self.c.get('/logout/')
        self.assertEqual(response.status_code, 302)
        response = self.c.get('/settings/')
        self.assertEqual(response.status_code, 302)

    def test_deactivate(self):
        response = self.c.get('/deactivate/')
        self.assertEqual(response.status_code, 302)

        loggedin = self.c.login(email=self.user_email, password = self.user_pwd)
        self.assertTrue(loggedin)
        
        response = self.c.get('/deactivate/')
        self.assertEqual(response.status_code, 200)

    def test_delete_address(self):
        response = self.c.get(f'/address/{self.address.id}/delete')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["location"], f'/login/?next=/address/{self.address.id}/delete')

        loggedin = self.c.login(email=self.user_email, password = self.user_pwd)
        self.assertTrue(loggedin)

        response = self.c.get(f'/address/{self.address.id}/delete')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["location"], '/settings/')

    def test_edit_address(self):
        response = self.c.post(f'/address/{self.address.id}/edit', {
            'country': DeliveryInfo.COUNTRIES[0][0],
            'state': DeliveryInfo.STATES[0][0],
            'zip': '1111',
            'address': 'edited_address',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["location"], f'/login/?next=/address/{self.address.id}/edit')

        loggedin = self.c.login(email=self.user_email, password = self.user_pwd)
        self.assertTrue(loggedin)

        response = self.c.post(f'/address/{self.address.id}/edit', {
            'country': DeliveryInfo.COUNTRIES[0][0],
            'state': DeliveryInfo.STATES[0][0],
            'zip': '1111',
            'address': 'edited_address',
        })
        self.assertEqual(response.status_code, 200)






"""class TestMainView(TestCase):
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
            new=True,
            promo=False
        )
        cls.product_variant_c = ProductVariant.objects.create(
            product=cls.product_a,
            size=42,
            color=cls.color_b,
            available_units=0,
            sale=True,
            new=True,
            promo=False
        )
        cls.product_variant_d = ProductVariant.objects.create(
            product=cls.product_a,
            size=39,
            color=cls.color_b,
            available_units=1200,
            sale=True,
            new=False,
            promo=True
        )

    def setUp(self):
        self.c = Client()

    def test_promo(self):
        response = self.c.get('/')
        self.assertEqual(len(response.context['promo']), 2)

    def test_new(self):
        response = self.c.get('/')
        self.assertEqual(len(response.context['new']), 3)
"""