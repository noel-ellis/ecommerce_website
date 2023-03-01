from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.main, name='main'),
    path('store', views.product_list_view, name='store'),
    path('new_collection', views.CollectionCreateView.as_view(), name='collection-create'),
    path('collections/<slug:slug>', views.collection_list, name='collection'),
    path('new_product', views.ProductCreateView.as_view(), name='product-create'),
    path('store/<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('store/<slug:slug>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('store/<slug:slug>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
]
