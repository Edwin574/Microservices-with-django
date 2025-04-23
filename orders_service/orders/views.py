from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderItemSerializer

# Create your views here.

class OrderFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status')
    min_total = filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    max_total = filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['status', 'payment_status', 'user_id']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    filterset_class = OrderFilter
    search_fields = ['id', 'tracking_number']
    ordering_fields = ['created_at', 'total_amount', 'status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        queryset = super().get_queryset()
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['post'])
    def update_payment_status(self, request, pk=None):
        order = self.get_object()
        payment_status = request.data.get('payment_status')
        
        if payment_status not in ['PENDING', 'PAID', 'FAILED']:
            return Response(
                {'error': 'Invalid payment status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.payment_status = payment_status
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['post'])
    def add_tracking(self, request, pk=None):
        order = self.get_object()
        tracking_number = request.data.get('tracking_number')
        
        if not tracking_number:
            return Response(
                {'error': 'Tracking number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.tracking_number = tracking_number
        order.status = 'SHIPPED'
        order.save()
        return Response(OrderSerializer(order).data)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    
    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs['order_pk'])
