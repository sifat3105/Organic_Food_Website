from django.db import models
from django.conf import settings
from Product.models import Product  # Assuming you have a Product model in a separate app

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'OrderItem {self.id}'
