from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.summary, name='summary'),
    path('add/', views.add, name='add')
]
