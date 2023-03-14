from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.main, name='main'),
    path('store', views.product_list_view, name='store'),
    path('categories', views.category_list, name='categories'),
    path('categories/<slug:slug>/update', views.CategoryUpdateView.as_view(), name='category-update'),
    path('store/<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('store/<slug:slug>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('store/<slug:slug>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
]
