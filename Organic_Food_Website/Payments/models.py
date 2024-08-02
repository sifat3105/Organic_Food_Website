from django.db import models
from Orders.models import Order  # Assuming you have an Order model

class Payment(models.Model):
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)  # e.g., 'Credit Card', 'PayPal'
    status = models.CharField(max_length=50)  # e.g., 'Completed', 'Pending', 'Failed'

    def __str__(self):
        return f'Payment {self.id} for Order {self.order.id}'
