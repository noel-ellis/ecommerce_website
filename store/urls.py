from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('products/create', views.ProductCreateView.as_view(), name='product-create'),
    path('products/', views.ProductListView.as_view(), name='product'),
    path('products/<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
]