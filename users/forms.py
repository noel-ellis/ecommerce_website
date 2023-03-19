from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import UserBase, DeliveryInfo


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(
        attrs={
            'class': 'form-control mb-2', 
            'type': 'email',
            'placeholder': 'Email'
        }
    ))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control mb-2', 
            'type': 'password',
            'placeholder': 'Password'
        }
    ))
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control mb-2', 
            'type': 'password',
            'placeholder': 'Confirm Password'
        }
    ))

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


class DeliveryInfoForm(forms.ModelForm):
    COUNTRIES = [('US', 'United States')]
    STATES = [('GA', 'Georgia')]
    country = forms.ChoiceField(label="Country", choices=COUNTRIES)
    state = forms.ChoiceField(label="State", choices=STATES)
    zip = forms.CharField(label="Zip")
    address = forms.CharField(label="Address")

    class Meta:
        model = DeliveryInfo
        fields = ['country', 'state', 'zip', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update(
            {'class': 'form-control mb-2', 'id': 'address-form-country'}
        )
        self.fields['state'].widget.attrs.update(
            {'class': 'form-control mb-2', 'id': 'address-form-state'}
        )
        self.fields['zip'].widget.attrs.update(
            {'class': 'form-control mb-2', 'id': 'address-form-zip'}
        )
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control mb-2', 'id': 'address-form-address'}
        )


class UserUpdateForm(forms.ModelForm):
    name = forms.CharField(label="First Name")
    surname = forms.CharField(label="Last Name")
    phone_number = forms.CharField(label='Phone Number')

    class Meta:
        model = UserBase
        fields = ['name', 'surname', 'phone_number']

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


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(
        attrs={
            'class': 'form-control', 
            'type': 'email',
            'placeholder': 'Email'
        }
    ))

    class Meta:
        fields = ['email']

    