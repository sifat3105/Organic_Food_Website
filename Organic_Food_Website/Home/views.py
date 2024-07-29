from django.shortcuts import render

# Create your views here.

def home_view(request):
    return render(request, 'home/home.html')


def check_view(request):
    return render(request, 'check.html')