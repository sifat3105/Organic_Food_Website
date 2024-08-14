from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import product_view, product_create, ajax_load_subcategories

urlpatterns = [
    path('<uuid:uuid>/', product_view, name= 'product'),
    path('create/', product_create, name='product_create'),
    path('ajax/load-subcategories/', ajax_load_subcategories, name='ajax_load_subcategories'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)