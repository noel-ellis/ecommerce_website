from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.main, name='main'),
    path('store', views.ProductListView.as_view(), name='store'),
    path('store/<slug:slug>', views.product_detail_view, name='product-detail'),
]
