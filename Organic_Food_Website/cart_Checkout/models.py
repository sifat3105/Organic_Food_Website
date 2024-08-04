from django.db import models
from django.conf import settings
from Product.models import Product 
from decimal import Decimal

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart {self.id} for {self.user.username}'
    

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_shipping_fee(cart):
        shipping_fee = 10.00
        desi_ship = Decimal(shipping_fee)
        cart_total_price = cart.get_total_price()
        total_price = cart_total_price + desi_ship
        total_price_percentage = min(round(cart_total_price / 5), 100)
        
        if total_price_percentage == 100:
            total_price = cart_total_price
            shipping_fee = Decimal('0.00')
        
        return shipping_fee
    
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=1)

    def __str__(self):
        return f'CartItem {self.product.name} in Cart {self.cart.user.first_name}'

    def get_total_price(self):
        return self.product.new_price * self.quantity
    
    def get_product_image(self):
        return self.product.images.first().image.url if self.product.images.exists() else None
