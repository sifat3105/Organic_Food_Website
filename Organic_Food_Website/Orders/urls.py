from django.urls import path 
from .views import order_create, generate_invoice_pdf

urlpatterns = [
    path('create/', order_create, name= 'order'),
    path('<int:order_id>/invoice/', generate_invoice_pdf, name='generate_invoice_pdf'),
]
