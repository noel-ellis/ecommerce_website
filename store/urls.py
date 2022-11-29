from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('create', views.StockCreateView.as_view(), name='stock-create'),
    path('', views.StockListView.as_view(), name='stock'),
    path('<int:pk>', views.StockDetailView.as_view(), name='stock-detail'),
    path('<int:pk>/update', views.StockUpdateView.as_view(), name='stock-update'),
    path('<int:pk>/delete', views.StockDeleteView.as_view(), name='stock-delete'),
]