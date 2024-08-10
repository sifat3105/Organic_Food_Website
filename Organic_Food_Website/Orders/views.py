from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from cart_Checkout.models import Cart, CartItem
from Account_Dashboard.models import ShippingAddress, BillingAddress


# Create your views here.

@csrf_exempt
def order_create(request):
    cart = get_object_or_404(Cart, user = request.user)
    cartitem = CartItem.objects.filter(cart = cart)
    order = Order.objects.create(
        user = request.user,
        shipping_address = get_object_or_404(ShippingAddress, user= request.user),
        billing_address = get_object_or_404(BillingAddress, user= request.user),
        total_price = cart.get_total_price(),
    )
    for item in cartitem:
        if item.quantity:
            price = item.product.new_price * item.quantity
        orderitem, Created = OrderItem.objects.get_or_create(
            order = order,
            product = item.product,
            price = price,
            quantity = item.quantity
        )
        item.delete()
        
        
    return redirect('home')

