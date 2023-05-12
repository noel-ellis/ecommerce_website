from django.urls import path

from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.summary, name='summary'),
    path('modify/', views.ModifyWishlist.as_view(), name='modify')
]
