from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate, get_user_model, update_session_auth_hash, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from .models import profile
from .forms import UserRegistrationForm, UserLoginForm
from .tokens import email_verification_token
# Create your views here.

User = get_user_model()


def sign_in_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'auth/sign_in.html', {'form':form})

def sign_up_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('email_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            })
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            return redirect('email_verification_sent')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/sign_up.html',{'form':form})


def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
        if email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            # Optionally, log the user in after activation
            login(request, user)
            return redirect('home')  # Redirect to the home page or a success page
        else:
            return HttpResponse('Activation link is invalid!')
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        return HttpResponse('Activation link is invalid!')