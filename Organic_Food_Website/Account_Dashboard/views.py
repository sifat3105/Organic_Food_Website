from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

def account_dashboard(request, username):
    context = {
        'username':username,
    }
    return render(request, 'account/account_dashboard.html',context)