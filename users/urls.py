from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import UserLoginForm, PwdResetForm

app_name = 'users'

urlpatterns = [
    path('settings/', views.settings, name='settings'),
    path('address/<slug:address_id>/edit', views.edit_address, name='edit_address'),
    path('address/<slug:address_id>/delete', views.delete_address, name='delete_address'),
    path('signup/', views.signup, name='signup'),
    path('activate/<slug:uidb64>/<slug:token>', views.activate, name='activate'),
    path("login/", auth_views.LoginView.as_view(template_name='users/login.html', form_class=UserLoginForm), name='login'),
    path("logout/", views.signout, name='logout'),
    path('deactivate/', views.deactivate, name='deactivate'),
    path("password-reset/",
         auth_views.PasswordResetView.as_view(
             template_name='users/pwd_reset/password_reset.html',
             form_class=PwdResetForm,
             email_template_name='users/pwd_reset/pwd_reset_email.html',
             success_url='done'
         ),
         name='password_reset'
         ),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/pwd_reset/password_reset_complete.html'),
         name='password_reset_complete'
         ),
    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/pwd_reset/password_reset_done.html'
         ),
         name='password_reset_done'
         ),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/pwd_reset/password_reset_confirm.html',
             success_url='/password-reset-complete/'
         ),
         name='password_reset_confirm'
         )
]
