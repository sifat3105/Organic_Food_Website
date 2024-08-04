from django.urls import path 
from .views import ssl_payment, payment_failed, payment_success, payment_cancel


urlpatterns = [
    path('', ssl_payment, name='payment'),
    path('failed/', payment_failed, name='payment_failed'),
    path('success/', payment_success, name='payment_success'),
    path('cancel/', payment_cancel, name='payment_cancel'),
]
