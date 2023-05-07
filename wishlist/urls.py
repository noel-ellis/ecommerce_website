from django.urls import path

from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.summary, name='summary'),
    path('modify/', views.modify, name='modify')
]
