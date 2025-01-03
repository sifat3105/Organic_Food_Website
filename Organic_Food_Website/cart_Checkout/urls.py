from django.urls import path
from .views import create_cart, cart_view, remove_from_cart, checkout_view

urlpatterns = [
    path('', cart_view, name='cart'),
    path("checkout/", checkout_view, name="checkout"),
    path('create/<uuid:product_uuid>/', create_cart, name='create_cart'),
    path('remove_from_cart/<int:item_id>', remove_from_cart, name='remove_from_cart'),
]