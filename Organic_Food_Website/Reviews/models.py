from django.db import models
from django.conf import settings
from Product.models import Product  

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # Assuming a rating scale of 1-5
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        unique_together = ('product', 'user')

    def __str__(self):
        return f'Review {self.id} for Product {self.product.name}'
