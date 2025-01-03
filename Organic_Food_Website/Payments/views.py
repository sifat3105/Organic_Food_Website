from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from sslcommerz_lib import SSLCOMMERZ
from decimal import Decimal
from cart_Checkout.models import Cart
from Orders.models import Order
import logging


            
           


logger = logging.getLogger(__name__)
def ssl_payment(request):
    cart = get_object_or_404(Cart, user = request.user)
    total_amount = cart.get_total_price() + Decimal(cart.get_shipping_fee())
    current_site = get_current_site(request)          
    domain=current_site.domain
    
    from sslcommerz_lib import SSLCOMMERZ 
    settings = { 'store_id': 'acb66a8f8a1790cf', 'store_pass': 'acb66a8f8a1790cf@ssl', 'issandbox': True }
    sslcommez = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = 100.26
    post_body['currency'] = "BDT"
    post_body['tran_id'] = "12345"
    post_body['success_url'] = f"http://{domain}/payment/success/"
    post_body['fail_url'] = f"http://{domain}/payment/failed/"
    post_body['cancel_url'] = f"http://{domain}/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = "test"
    post_body['cus_email'] = "test@test.com"
    post_body['cus_phone'] = "01790166212"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"


    response = sslcommez.createSession(post_body)
    print(response)
    return redirect(response['GatewayPageURL'])




def payment_failed(request):
    return render(request, 'payment/payment_failed.html')

@csrf_exempt
def payment_success(request):
    
    return redirect('order')
    # return render(request, 'payment/payment_success.html')

def payment_cancel(request):
    return render(request, 'payment/payment_cancel.html')
