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
