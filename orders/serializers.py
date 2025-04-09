from rest_framework import serializers
from .models import Order, OrderItem
from product_catalog.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'created_at']
        read_only_fields = ['price', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_amount', 'shipping_address', 'items', 'created_at', 'updated_at']
        read_only_fields = ['status', 'total_amount', 'created_at', 'updated_at'] 