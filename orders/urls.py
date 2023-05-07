from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('new/', views.new_order, name='new'),
    path('orderplaced/', views.orderplaced, name='order-placed')
]
