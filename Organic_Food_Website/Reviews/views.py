from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .models import Product,Review
from .forms import ReviewForm

def submit_review(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_exists = Review.objects.filter(product=product, user=user).exists()
            if review_exists:
                messages.error(request, 'You have already submitted a review for this product.')
                return redirect('product', uuid=product.uuid)

            review = form.save(commit=False)
            review.product = product
            review.user = user
            try:
                review.save()
                messages.success(request, 'Review submitted successfully!')
                return redirect('product', uuid=product.uuid)
            except IntegrityError:
                messages.error(request, 'A review by this user for this product already exists.')
                return redirect('product', uuid=product.uuid)

        messages.error(request, 'Invalid form data.')
        return redirect('product', uuid=product.uuid)

    return redirect('product', uuid=product.uuid)


def product_reviews( product_uuid):
    product = get_object_or_404(Product, uuid = product_uuid)
    reviews = Review.objects.filter(product=product)
    ratings = Review.objects.filter(product=product).values_list('rating', flat=True)
    total_rating = sum(ratings)
    rating_out_of_5 = total_rating/ len(ratings)
    
    return {
        'reviews':reviews,
        'rating_out_of_5':rating_out_of_5
    }


