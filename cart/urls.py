from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.summary, name='summary'),
    path('modify/', views.ModifyCart.as_view(), name='modify')
]
