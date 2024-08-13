from django.db import models

class DashboardAnalytics(models.Model):
    date = models.DateField()
    total_users = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    new_users = models.PositiveIntegerField(default=0)
    new_orders = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_refunds = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    canceled_orders = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Analytics for {self.date}"
