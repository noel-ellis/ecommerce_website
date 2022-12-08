from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('create', views.ProductCreateView.as_view(), name='product-create'),
    path('', views.ProductListView.as_view(), name='product'),
    path('<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
]