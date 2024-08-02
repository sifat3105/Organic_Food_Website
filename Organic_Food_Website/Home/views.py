from django.shortcuts import render, get_object_or_404
from Product.models import Product , Category
from Reviews.views import product_reviews

# Create your views here.

def home_view(request):
    category_oranges = Category.objects.filter(name='Oranges').first()
    category_grapes = Category.objects.filter(name='Grapes').first()
    category_blueberries = Category.objects.filter(name='Blueberries').first()
    category_lemon = Category.objects.filter(name='Lemon').first()
    category_vegetables = Category.objects.filter(name='Vegetables').first()

    products_oranges = Product.objects.filter(category=category_oranges) if category_oranges else Product.objects.none()
    products_grapes = Product.objects.filter(category=category_grapes) if category_grapes else Product.objects.none()
    products_blueberries = Product.objects.filter(category=category_blueberries) if category_blueberries else Product.objects.none()
    products_lemon = Product.objects.filter(category=category_lemon) if category_lemon else Product.objects.none()
    products_vegetables = Product.objects.filter(category=category_vegetables) if category_vegetables else Product.objects.none()
    
    return render(request, 'home/home.html', locals())


def check_view(request):
    print(product_reviews('30ebd947-a615-4c54-b302-b6778e73f6b7'))
    return render(request, 'check.html')