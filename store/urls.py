from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product'),
    path('new_category', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<slug:slug>', views.category_list, name='category'),
    path('new_product', views.ProductCreateView.as_view(), name='product-create'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('<slug:slug>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('<slug:slug>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
]
