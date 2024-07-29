from django.urls import path
from .views import home_view, check_view

urlpatterns = [
    path('', home_view, name='home'),
    path('check',check_view, name='check'),
]
