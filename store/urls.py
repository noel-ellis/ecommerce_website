from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('stock', views.StockListView.as_view(), name='stock'),
    path('', views.home, name='home'),
]