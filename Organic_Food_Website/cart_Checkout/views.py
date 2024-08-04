from django.shortcuts import render,redirect, get_object_or_404 
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal
from Account_Dashboard.models import ShippingAddress, Account
from Account_Dashboard.forms import ShippingAddressForm
from .context_processors import cart_view
from .models import Cart, CartItem, Product

# Create your views here.


def create_cart(request, product_uuid):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, uuid=product_uuid)
    cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cartitem.quantity += 1
        cartitem.price +=product.new_price
        cartitem.save()
    else:
        cartitem.price = product.new_price
        cartitem.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if request.method == "POST":
        for item in cart_items:
            new_quantity = request.POST.get(f'qty{item.id}')
            if new_quantity:
                try:
                    new_quantity = int(new_quantity)
                    if new_quantity != item.quantity:
                        cart_item = get_object_or_404(CartItem, id=item.id)
                        cart_item.quantity = new_quantity
                        cart_item.save()
                except ValueError:
                    pass
    shipping_fee = 10.00
    desi_ship = Decimal(shipping_fee)
    cart_total_price = cart.get_total_price()
    total_price = cart_total_price + desi_ship
    total_price_percentage = min(round(cart_total_price / 5), 100)
    
    if total_price_percentage == 100:
        total_price = cart_total_price
        shipping_fee = '0.00'
        
    return render(request, 'cart/cart.html', {
        'total_price':total_price,
        'total_price_percentage':total_price_percentage,
        'shipping_fee':shipping_fee
    })



def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def checkout_view(request):
    account, created = Account.objects.get_or_create(user=request.user)
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
        form_title = "Update Shipping Address"
    except ShippingAddress.DoesNotExist:
        shipping_address = None
        form_title = "Create Shipping Address"
    
    if request.method == "POST":
        number = request.POST.get('number')
        checkbox = request.POST.get('flexRadioDefault')
        account.phone_number = number
        account.save()
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('payment')
    else:
        form = ShippingAddressForm(instance=shipping_address)
        
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    shipping_fee = Decimal(cart.get_shipping_fee())
    sub_total = cart.get_total_price ()
    total_price = sub_total + shipping_fee
    return render(request, 'cart/checkout.html', {
        'shipping_address':shipping_address,
        'form':form,
        'cart':cart,
        'cart_items':cart_items,
        'shipping_fee':shipping_fee,
        'total_price':total_price
    })
    
