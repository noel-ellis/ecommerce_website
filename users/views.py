from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignUpForm
from django.contrib.auth.decorators import login_required

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
    return render(request, "users/settings.html")
