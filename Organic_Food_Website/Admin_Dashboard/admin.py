from django.contrib import admin
from .models import DashboardAnalytics

@admin.register(DashboardAnalytics)
class DashboardAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'total_users', 'total_orders', 'total_revenue', 'new_users', 'new_orders',
        'total_sales', 'total_refunds', 'canceled_orders'
    ]
    search_fields = ['date']
    list_filter = ['date']
