from django.urls import path
from . views import sign_in_view, sign_up_view, activate_account, email_verification_sent, password_reset_mail_sended, ResetPasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sign-in/', sign_in_view, name= 'signin'),
    path('sign-up/', sign_up_view, name= 'signup'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('email_verification_sent/', email_verification_sent, name='email_verification_sent'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-mail-sended/', password_reset_mail_sended, name= 'password_reset_mail_sended'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset/password_reset_complete.html'), name='password_reset_complete'),
    

]
