from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from Reviews.views import product_reviews
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import SubCategory


# Create your views here.

def product_view(request, uuid):
    product = get_object_or_404(Product, uuid=uuid)
    product_review = product_reviews(uuid)
    rating = product.rating
    if rating is None:
        rating_percentage = 0
    else:
        rating_percentage = rating * 20
    return render(request, 'product/single_product.html',{
        'product':product,
        'rating_percentage':rating_percentage,
        'product_review':product_review,
    })


from django.urls import reverse
from .models import Product, ProductImage
from .forms import ProductForm  
from django.http import HttpRequest

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            return redirect(reverse('home'))  # Change to your product list view name
    else:
        form = ProductForm()

    context = {
        'form': form,
    }
    return render(request, 'product/product_form.html', context)



def ajax_load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'products/subcategory_dropdown_list_options.html', {'subcategories': subcategories})

