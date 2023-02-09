from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserBase


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = UserBase
        fields = ['email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = UserBase
        fields = ['email', 'name', 'surname', 'phone_number', 'country', 'city', 'postcode', 'address_1', 'address_2']
