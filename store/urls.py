from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('categories/create', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<slug:slug>', views.category_list, name='category'),
    path('products/create', views.ProductCreateView.as_view(), name='product-create'),
    path('', views.ProductListView.as_view(), name='product'),
    path('products/<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<slug:slug>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<slug:slug>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
]
