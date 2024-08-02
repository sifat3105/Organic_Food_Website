from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from collections import Counter
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
    rating_out_of_5 = sum(ratings)/ len(ratings)
    if rating_out_of_5 not in {5, 4, 3, 2, 1}:
            rating_out_of_5 = round(rating_out_of_5,1)
    
    counter = Counter(ratings)
    total_ratings = sum(counter.values())
    star_5 = counter.get(5, 0)
    star_4 = counter.get(4, 0)
    star_3 = counter.get(3, 0)
    star_2 = counter.get(2, 0)
    star_1 = counter.get(1, 0)
    star_5_percent = round(int((star_5 / total_ratings) * 100)) if total_ratings > 0 else 0
    star_4_percent = round(int((star_4 / total_ratings) * 100)) if total_ratings > 0 else 0
    star_3_percent = round(int((star_3 / total_ratings) * 100)) if total_ratings > 0 else 0
    star_2_percent = round(int((star_2 / total_ratings) * 100)) if total_ratings > 0 else 0
    star_1_percent = round(int((star_1 / total_ratings) * 100)) if total_ratings > 0 else 0
    stars = {
    'star_5': star_5,
    'star_4': star_4,
    'star_3': star_3,
    'star_2': star_2,
    'star_1': star_1,
    'star_5_percent': star_5_percent,
    'star_4_percent': star_4_percent,
    'star_3_percent': star_3_percent,
    'star_2_percent': star_2_percent,
    'star_1_percent': star_1_percent,
    }

        
            
    
    return {
        'reviews':reviews,
        'rating_out_of_5':rating_out_of_5,
        'stars':stars,
        'total_ratings':total_ratings,
    }


