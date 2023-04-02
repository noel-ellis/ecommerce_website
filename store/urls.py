from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.main, name='main'),
    path('store', views.product_list_view, name='store'),
    path('store/<slug:slug>', views.product_detail_view, name='product-detail'),
    path('store/<slug:slug>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('store/<slug:slug>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
]
