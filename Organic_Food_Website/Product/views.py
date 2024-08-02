from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def product_view(request, uuid):
    product = get_object_or_404(Product, uuid=uuid)
    rating = product.rating
    if rating is None:
        rating_percentage = 0
    else:
        rating_percentage = rating * 20
    return render(request, 'product/single_product.html',{
        'product':product,
        'rating_percentage':rating_percentage
    })



