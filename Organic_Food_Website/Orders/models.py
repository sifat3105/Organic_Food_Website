from django.db import models
from django.conf import settings
from Product.models import Product
from Account_Dashboard.models import ShippingAddress, BillingAddress

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_total_price(self):
        return self.product.new_price * self.quantity

    def __str__(self):
        return f'OrderItem {self.id} for Order {self.order.id}'
    
    def get_product_image(self):
        return self.product.images.first().image.url if self.product.images.exists() else None
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
class fail_order(models.Model):
    name = models.CharField( max_length=50)
