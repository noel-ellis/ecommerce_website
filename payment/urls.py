from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('webhook/', views.stripe_webhook),
    ]