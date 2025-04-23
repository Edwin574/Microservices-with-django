from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'status', 'total_amount', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['id', 'user_id', 'tracking_number']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product_name', 'quantity', 'unit_price', 'total_price']
    list_filter = ['created_at']
    search_fields = ['product_name', 'order__id']
    readonly_fields = ['total_price', 'created_at']
