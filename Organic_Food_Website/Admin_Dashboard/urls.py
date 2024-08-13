from django.urls import path
from .views import dashboard_view, chart_data

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('chart-data/', chart_data, name='chart_data'),
]
