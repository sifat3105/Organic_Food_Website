from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
from .models import DashboardAnalytics
from Orders.models import Order


def dashboard_view(request):
    analytics = DashboardAnalytics.objects.order_by('-date')[:7]
    labels = [entry.date.strftime('%Y-%m-%d') for entry in analytics]
    data = [entry.total_sales for entry in analytics]
    dashboard_create()
    return render(request, 'admin_dashboard/dashboard.html', {
        'labels': labels,
        'data': data,
    })
    
    
    
    
def dashboard_create():
    today = timezone.now().date()
    total_seles =sum( Order.objects.all().values_list('total_price', flat=True))
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    today = timezone.now().date()
    new_users = User.objects.filter(date_joined__date=today).count()
    new_orders = Order.objects.filter(created__date=today).count()
    
    analytics, Created = DashboardAnalytics.objects.get_or_create(date = today)
    analytics.total_orders =total_orders
    analytics.total_sales = total_seles
    analytics.total_users = total_users
    analytics.new_orders = new_orders
    analytics.new_users = new_users
    analytics.save()
    
    print(total_orders)
    
    return


def chart_data(request):
    analytics = DashboardAnalytics.objects.all().order_by('date')
    data = {
        "labels": [analytics.date.strftime("%Y-%m-%d") for analytics in analytics],
        "total_users": [analytics.total_users for analytics in analytics],
        "total_orders": [analytics.total_orders for analytics in analytics],
        "total_revenue": [float(analytics.total_revenue) for analytics in analytics],
        "new_users": [analytics.new_users for analytics in analytics],
        "new_orders": [analytics.new_orders for analytics in analytics],
        "total_sales": [float(analytics.total_sales) for analytics in analytics],
        "total_refunds": [float(analytics.total_refunds) for analytics in analytics],
        "canceled_orders": [analytics.canceled_orders for analytics in analytics],
    }
    return JsonResponse(data)
