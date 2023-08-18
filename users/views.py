# ORDERED ITEM CHANGE; ordered_items

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserSignUpForm, UserUpdateForm, DeliveryInfoForm
from .models import UserBase, DeliveryInfo
from .token import account_activation_token
from orders.models import Order
from store.models import Product


class UserSignup(View):

    def redirect_authenticated_users(self, request):
        if request.user.is_authenticated:
            return redirect('users:settings')

    def post(self, request):
        self.redirect_authenticated_users(request)

        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.set_password = form.cleaned_data.get('password')
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string('users/signup/AccountActivationEmail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject=subject, message=message)

            messages.success(request, f'Success! We have sent you a confirmation email')
            return redirect('users:login')
        return render(request, 'users/signup.html', {'form': form})

    def get(self, request):
        self.redirect_authenticated_users(request)

        form = UserSignUpForm()
        return render(request, 'users/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        return render(request, 'users/signup/AccountActivationFailed.html')

    if user is not None and (account_activation_token.check_token(user, token)):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, f'Email confirmed')
        return redirect('users:settings')
    return render(request, 'users/signup/AccountActivationFailed.html')


@login_required
def deactivate(request):
    user = request.user
    logout(request)
    user.is_active = False
    user.save()
    return render(request, 'users/AccountSuccessfullyDeactivated.html')


@login_required
def signout(request):
    logout(request)
    messages.success(request, 'Signed out')
    return redirect('users:login')


class EditAddress(LoginRequiredMixin, View):

    def post(self, request, address_id):
        user = request.user
        address = DeliveryInfo.objects.filter(id=address_id).first()
        if not address:
            messages.error(request, "Address doesn't exist")
            return redirect('users:settings')

        if address.user != user:
            messages.error(request, 'No permission')
            return redirect('users:settings')

        if "address_data" in request.POST:
            form = DeliveryInfoForm(
                request.POST,
                instance=address
            )

            if form.is_valid():
                form.save()
                messages.success(request, 'Address Updated')
                return redirect('users:settings')

            messages.error(request, 'Data is invalid')
            return redirect('users:settings')

        address_form = DeliveryInfoForm(instance=address)

        context = {
            'address_form': address_form
        }

        return render(request, "users/edit_address.html", context)

    def get(self, request, address_id):
        user = request.user
        address = DeliveryInfo.objects.filter(id=address_id).first()
        if not address:
            messages.error(request, "Address doesn't exist")
            return redirect('users:settings')

        if address.user != user:
            messages.error(request, 'No permission')
            return redirect('users:settings')

        address_form = DeliveryInfoForm(instance=address)

        context = {
            'address_form': address_form
        }

        return render(request, "users/edit_address.html", context)


@login_required
def delete_address(request, address_id):
    user = request.user
    address = DeliveryInfo.objects.filter(id=address_id).first()
    if not address:
        messages.error(request, "Address doesn't exist")
        return redirect('users:settings')

    if address.user != user:
        messages.error(request, 'No permission')
        return redirect('users:settings')

    address.delete()

    messages.success(request, 'Deleted')
    return redirect('users:settings')


class Settings(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        address_form = DeliveryInfoForm()
        address_info = DeliveryInfo.objects.filter(user=request.user.id).all()

        order_quiery = Order.objects.filter(user=request.user.id)
        order_history = {}

        for order in order_quiery:
            ordered_items_data = {}
            total_price = 0

            for ordered_item in order.ordered_items.all():
                
                product_quiery = Product.objects.get(pk=ordered_item.product_variant.product_id) # ORDERED ITEM CHANGE; TODO: TO BE CHANGED
                product_name = product_quiery.name
                product_slug = product_quiery.slug

                # ORDERED ITEM CHANGE; ordered_item_data from settings.html
                ordered_item_data = {
                    'price': ordered_item.price,
                    'quantity': ordered_item.quantity,
                    'product_name': product_name,
                    'product_slug': product_slug
                }
                # ORDERED ITEM CHANGE; key is not being used in settings.html
                ordered_items_data[ordered_item.product_variant_id] = ordered_item_data # ORDERED ITEM CHANGE; TODO: TO BE CHANGED

                ordered_item_total = ordered_item.price*ordered_item.quantity
                total_price += ordered_item_total

            delivery_info_data = {
                'country': order.delivery_info.country,
                'state': order.delivery_info.state,
                'zip': order.delivery_info.zip,
                'address': order.delivery_info.address
            }

            # ORDERED ITEM CHANGE; order in settings.html
            order_data = {
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'paid': order.paid,
                'status': order.status,
                'delivery_info': delivery_info_data,
                'ordered_items': ordered_items_data,
                'total_price': total_price
            }

            order_history[order.id] = order_data

        context = {
            'user_form': user_form,
            'address_form': address_form,
            'address_info': address_info,
            'order_history': order_history # ORDERED ITEM CHANGE; TODO: map the structure
        }

        return render(request, "users/settings.html", context)

    def post(self, request):
        if "profile_data" in request.POST:
            form = UserUpdateForm(
                request.POST,
                instance=request.user
            )

            if form.is_valid():
                form.save()
                messages.success(request, 'Updated')
                return redirect('users:settings')

            messages.error(request, 'Data is invalid')
            return redirect('users:settings')

        if "delivery_info" in request.POST:
            form = DeliveryInfoForm(
                request.POST
            )

            if form.is_valid():
                form = form.save(commit=False)
                form.user_id = request.user.id
                form.save()
                messages.success(request, 'New address has been added')
                return redirect('users:settings')

            messages.error(request, 'Data is invalid')
            return redirect('users:settings')
