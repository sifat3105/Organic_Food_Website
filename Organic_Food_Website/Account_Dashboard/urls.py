from django.urls import path
from .views import account_dashboard



urlpatterns = [
    path('<str:username>/',account_dashboard, name= 'account')
]
