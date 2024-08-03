from django.contrib import admin
from .models import Account, ShippingAddress, BillingAddress
# Register your models here.
admin.site.register(Account)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
