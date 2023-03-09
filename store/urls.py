from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.main, name='main'),
    path('store', views.product_list_view, name='store'),
    path('new_category', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories', views.category_list, name='categories'),
    path('new_product', views.ProductCreateView.as_view(), name='product-create'),
    path('store/<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('store/<slug:slug>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('store/<slug:slug>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
]
