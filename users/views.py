from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, logout

from .forms import UserSignUpForm, UserUpdateForm
from .models import UserBase
from .token import account_activation_token


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
    messages.success(request, 'Your account has been deactivated')
    return redirect('store:main')


def signup(request):
    if request.user.is_authenticated:
        return redirect('users:settings')

    if request.method == "POST":
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

    form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def settings(request):
    if request.method == "POST":
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

    form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, "users/settings.html", context)
