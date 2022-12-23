from django.test import TestCase, Client
from .models import Profile
from django.contrib.auth.models import User
from PIL import Image

class TestProfileModel(TestCase):
    def setUp(self):
        self.c = Client()
        self.username = 'admin'
        self.password = 'admin123'
        self.user = User.objects.create_superuser(username=self.username, password=self.password)
        self.profile = Profile.objects.get(user_id=self.user.id)

    def test_profile_model_return(self):
        self.assertEqual(str(self.profile), f'{self.user.username} Profile')

    def test_profile_thumbnail(self):
        self.c.login(username=self.username, password=self.password)
        old_path = self.profile.image.path
        new_path = 'media/stock_pics/J_mint_gold_art_nouveau_30it_4scale.png'
        # DOESN'T UPDATE | INCORRECT FORMAT (I GUESS)
        with open(new_path, 'rb') as img:
            response = self.c.post('/settings', 
                {
                    'username': self.username,
                    'email': 'blabla@gmail.com',
                    'address': 'blabla',
                    'image': img
                }
            )

        self.assertEqual(response.status_code, 301)
        img = Image.open(self.profile.image.path)
        self.assertNotEqual(old_path, self.profile.image.path)
        self.assertLessEqual(img.height, 300)
        self.assertLessEqual(img.width, 300)