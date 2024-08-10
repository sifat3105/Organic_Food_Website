from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_image', 'order', 'product', 'price', 'quantity')
    template = 'admin/orderitem_inline.html'

    def product_image(self, obj):
        image_url = obj.get_product_image()
        if image_url:
            return format_html('<img src="{}" style="width: 50px; height: auto;"/>', image_url)
        return 'No Image'
    product_image.short_description = 'Product Image'
    
    def get_readonly_fields(self, request, obj=None):
        # Ensure the product_image field is read-only
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        # Disable editing
        return False

    def has_add_permission(self, request, obj=None):
        # Disable adding new items
        return False

    def has_delete_permission(self, request, obj=None):
        # Disable deletion
        return False

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'updated', 'paid', 'total_price', 'transaction_id')
    list_filter = ('paid', 'created', 'updated')
    search_fields = ('user__username', 'transaction_id')
    inlines = [OrderItemInline]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_image', 'price', 'quantity')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__name')

    def product_image(self, obj):
        image_url = obj.get_product_image()
        if image_url:
            return format_html('<img src="{}" style="width: 50px; height: auto;"/>', image_url)
        return 'No Image'



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)


















# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 1  # Number of empty forms to display

# class OrderAdmin(admin.ModelAdmin):
#     inlines = [OrderItemInline]
#     fieldsets = (
#         (None, {
#             'fields': ('user',)
#         }),
#         ('Order Details', {
#             'fields': ('total_price', 'transaction_id', 'paid'),
#             'classes': ('collapse',),  # Makes this section collapsible
#         }),
#         ('Timestamps', {
#             'fields': ('created', 'updated'),
#             'classes': ('collapse',),  # Makes this section collapsible
#         }),
#     )
#     list_display = ('id', 'user', 'total_price', 'paid', 'created')
#     list_filter = ('paid', 'created')
#     search_fields = ('user__username', 'transaction_id')

# class FailOrderAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)

# # Register models with Django admin
# admin.site.register(Order, OrderAdmin)
# admin.site.register(fail_order, FailOrderAdmin)
