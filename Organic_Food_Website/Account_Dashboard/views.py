from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import ShippingAddress,BillingAddress, Account
from .utils import convert_image_size
from Orders.models import Order

def account_dashboard(request, username):
    if request.method == 'POST':
        img= request.FILES.get('image')
        account, created = Account.objects.get_or_create(user=request.user)
        image = convert_image_size(img)
        account.image = image 
        account.save()
    
    name = f'{request.user.first_name} {request.user.last_name}'
    email = request.user.email
    shippings = get_object_or_404(ShippingAddress, user = request.user)
    billings = get_object_or_404(BillingAddress, user = request.user)
    # account = get_object_or_404(Account, user = request.user)
    shipping = f'{shippings.country}, {shippings.state}, {shippings.city}, {shippings.street_address}'
    billing = f'{billings.country}, {billings.state}, {billings.city}, {billings.street_address}'
    address = {"shipping":shipping,"billing":billing}
    orders = Order.objects.filter(user = request.user)
        
    context = {
        
        'username':username,
        'name':name,
        'email':email,
        'address':address,
        
    }
    return render(request, 'account/account_dashboard.html',locals())




