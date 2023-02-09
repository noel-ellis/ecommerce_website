from django.contrib.auth.models import User
from django.db import models
from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'
