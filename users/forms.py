from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserBase


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(help_text='Required')
    password1 = forms.CharField(label="Password", help_text='Required', widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", help_text='Required', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ['email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(
        attrs={
            'class': 'form-control mb-2', 
            'type': 'email',
            'placeholder': 'Email'
        }
    ))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control mb-2', 
            'type': 'password',
            'placeholder': 'Password'
        }
    ))


class UserUpdateForm(forms.ModelForm):
    name = forms.CharField(label="Name")
    surname = forms.CharField(label="Surname")
    phone_number = forms.CharField(label="Phone number")
    country = forms.CharField(label="Country")
    city = forms.CharField(label="City")
    postcode = forms.CharField(label="Postcode")
    address_1 = forms.CharField(label="Address 1")
    address_2 = forms.CharField(label="Address 2")

    class Meta:
        model = UserBase
        fields = ['name', 'surname', 'phone_number', 'country', 'city', 'postcode', 'address_1', 'address_2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control mb-2'}
        )
        self.fields['surname'].widget.attrs.update(
            {'class': 'form-control mb-2'}
        )
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control mb-2'}
        )
        self.fields['country'].widget.attrs.update(
            {'class': 'form-control mb-2'}
        )
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control mb-2'}
        )
        self.fields['postcode'].widget.attrs.update(
            {'class': 'form-control mb-2'}
        )
        self.fields['address_1'].widget.attrs.update(
            {'class': 'form-control mb-2'}
        )
        self.fields['address_2'].widget.attrs.update(
            {'class': 'form-control mb-2'}
        )
