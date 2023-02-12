from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import UserLoginForm

app_name = 'users'

urlpatterns = [
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup, name='signup'),
    path('activate/<slug:uidb64>/<slug:token>', views.activate, name='activate'),
    path("login/", auth_views.LoginView.as_view(template_name='users/login.html', form_class=UserLoginForm), name='login'),
    path("logout/", views.signout, name='logout'),
    path('deactivate/', views.deactivate, name='deactivate'),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
        name='password_reset'
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    )
]
