from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('users', views.UsersListView.as_view(), name='users'),
    path('stock', views.StockListView.as_view(), name='stock'),
    path('', views.home, name='home'),
]