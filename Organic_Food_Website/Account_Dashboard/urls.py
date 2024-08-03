from django.urls import path
from .views import account_dashboard, update_profile_picture



urlpatterns = [
    path('<str:username>/',account_dashboard, name= 'account'),
    path('update-profile-picture/', update_profile_picture, name='update_profile_picture'),
]
