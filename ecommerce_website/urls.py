from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include('store.urls', namespace='store')),
    path("", include('users.urls', namespace='users')),
    path("cart/", include('cart.urls', namespace='cart')),
    path("wishlist/", include('wishlist.urls', namespace='wishlist')),
    path("payment/", include('payment.urls', namespace='payment')),
    path("orders/", include('orders.urls', namespace='orders')),
    path("admin/", admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings .MEDIA_ROOT)
