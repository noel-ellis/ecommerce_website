from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import UserSignUpForm, UserUpdateForm


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome, {username}! Please, log in')
            return redirect('users:login')
        return render(request, 'users/signup.html', {'form': form})

    form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def settings(request):
    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Updated')
            return redirect('users:settings')

        messages.error(request, 'Data is invalid')
        return redirect('users:settings')

    user_form = UserUpdateForm(instance=request.user)

    context = {
        'user_form': user_form,
    }

    return render(request, "users/settings.html", context)
