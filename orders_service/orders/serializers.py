from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_name', 'quantity', 'unit_price', 'total_price', 'created_at']
        read_only_fields = ['total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user_id', 'status', 'total_amount', 'shipping_address',
            'billing_address', 'created_at', 'updated_at', 'payment_status',
            'tracking_number', 'items'
        ]
        read_only_fields = ['created_at', 'updated_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'user_id', 'shipping_address', 'billing_address', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_amount = sum(
            item['quantity'] * item['unit_price']
            for item in items_data
        )
        
        order = Order.objects.create(
            **validated_data,
            total_amount=total_amount,
            status='PENDING',
            payment_status='PENDING'
        )

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order 