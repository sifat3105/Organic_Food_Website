from django.db import models
from django.contrib.auth import get_user_model




User = get_user_model()
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image  = models.ImageField(upload_to="profile_image/", max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    
    def __str__(self):
        return str(self.user.username)
    
    

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255, null=True, blank=True, default="123 Example Street")
    city = models.CharField(max_length=100, null=True, blank=True, default="Dhaka")
    state = models.CharField(max_length=100, null=True, blank=True, default="Dhaka Division")
    postal_code = models.CharField(max_length=20, null=True, blank=True, default="1212")
    country = models.CharField(max_length=100, null=True, blank=True, default="Bangladesh")
    number = models.CharField(max_length=25, null=True, blank=True, default="+8801234567890")

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.postal_code}, {self.country}"
    
class BillingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255, null=True, blank=True,default="street_address")
    city = models.CharField(max_length=100, null=True, blank=True, default="city")
    state = models.CharField(max_length=100, null=True, blank=True, default="state")
    postal_code = models.CharField(max_length=20, null=True, blank=True, default="postal_code")
    country = models.CharField(max_length=100, null=True, blank=True, default="country")
    number = models.CharField(max_length=25, null=True, blank=True, default="number")


    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.postal_code}, {self.country}"