from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        
        return self.create_user(email, password, **other_fields)
    
    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    name = models.CharField(max_length=150, blank=True)
    surname = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=150, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.email
    

class DeliveryInfo(models.Model):
    COUNTRIES = [('US', 'United States')]
    STATES = [('GA', 'Georgia')]

    user = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    country = models.CharField(max_length=2, blank=True, choices=COUNTRIES)
    state = models.CharField(max_length=2, blank=True, choices=STATES)
    zip = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f'{self.country}, {self.state}, {self.zip}, {self.address}'
