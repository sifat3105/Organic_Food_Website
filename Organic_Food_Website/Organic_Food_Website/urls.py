from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('authentication/',include('Auth_app.urls')),
    path('account/', include('Account_Dashboard.urls')),
    path('product/', include('Product.urls')),
    path('review/', include('Reviews.urls')),
    path('cart/', include('cart_Checkout.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)