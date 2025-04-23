from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

# Create your views here.

class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing shopping carts.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        return Cart.objects.filter(is_active=True)

    @swagger_auto_schema(
        operation_description="Add an item to the cart",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['product_id', 'unit_price'],
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_STRING),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
                'unit_price': openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        ),
        responses={200: CartSerializer}
    )
    @action(detail=True, methods=['post'])
    def add_item(self, request, user_id=None):
        cart = self.get_object()
        
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        unit_price = float(request.data.get('unit_price'))

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.unit_price = unit_price
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(
                cart=cart,
                product_id=product_id,
                quantity=quantity,
                unit_price=unit_price
            )

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update item quantity in the cart",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['product_id', 'quantity'],
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_STRING),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ),
        responses={
            200: CartSerializer,
            404: 'Item not found in cart'
        }
    )
    @action(detail=True, methods=['post'])
    def update_item(self, request, user_id=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity'))

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Remove an item from the cart",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['product_id'],
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: CartSerializer,
            404: 'Item not found in cart'
        }
    )
    @action(detail=True, methods=['post'])
    def remove_item(self, request, user_id=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Clear all items from the cart",
        responses={200: CartSerializer}
    )
    @action(detail=True, methods=['post'])
    def clear(self, request, user_id=None):
        cart = self.get_object()
        cart.items.all().delete()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new cart or get existing cart for a user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: CartSerializer,
            201: CartSerializer
        }
    )
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        
        # Check if an active cart already exists for the user
        existing_cart = Cart.objects.filter(user_id=user_id, is_active=True).first()
        if existing_cart:
            serializer = self.get_serializer(existing_cart)
            return Response(serializer.data)

        # Create new cart if none exists
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
