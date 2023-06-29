from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", include('store.urls', namespace='store')),
    path("", include('users.urls', namespace='users')),
    path("cart/", include('cart.urls', namespace='cart')),
    path("wishlist/", include('wishlist.urls', namespace='wishlist')),
    path("payment/", include('payment.urls', namespace='payment')),
    path("orders/", include('orders.urls', namespace='orders')),
    path("admin/", admin.site.urls)
]

urlpatterns += staticfiles_urlpatterns()
