from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup, name='signup'),
    path("login/", auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]