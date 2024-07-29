from django.urls import path
from . views import sign_in_view, sign_up_view, activate_account, email_verification_sent

urlpatterns = [
    path('sign-in/', sign_in_view, name= 'signin'),
    path('sign-up/', sign_up_view, name= 'signup'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('email_verification_sent/', email_verification_sent, name='email_verification_sent'),
]
