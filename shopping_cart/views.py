from rest_framework import generics, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from product_catalog.models import Product
from Microservices.swagger import cart_schema, cart_item_schema, error_response

class UserCartItemListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating cart items.
    
    GET: List all cart items for a user (filtered by user_id query parameter)
    POST: Create a new cart item
    """
    serializer_class = CartItemSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="Filter cart items by user ID",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: CartItemSerializer(many=True),
            201: CartItemSerializer()
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CartItemSerializer,
        responses={201: CartItemSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return CartItem.objects.filter(user_id=user_id)
        return CartItem.objects.all()

class UserCartItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting cart items.
    
    GET: Retrieve a specific cart item
    PUT: Update a specific cart item
    PATCH: Partially update a specific cart item
    DELETE: Delete a specific cart item
    """
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    @swagger_auto_schema(
        responses={200: CartItemSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CartItemSerializer,
        responses={200: CartItemSerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CartItemSerializer,
        responses={200: CartItemSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={204: "No content"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        responses={
            200: CartSerializer,
            401: error_response
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            200: CartSerializer,
            401: error_response,
            404: error_response
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=cart_schema,
        responses={
            201: CartSerializer,
            400: error_response,
            401: error_response
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=cart_schema,
        responses={
            200: CartSerializer,
            400: error_response,
            401: error_response,
            404: error_response
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=cart_schema,
        responses={
            200: CartSerializer,
            400: error_response,
            401: error_response,
            404: error_response
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            204: 'No content',
            401: error_response,
            404: error_response
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()
        return CartItem.objects.filter(cart__user=self.request.user)

    @swagger_auto_schema(
        responses={
            200: CartItemSerializer(many=True),
            401: error_response
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            200: CartItemSerializer,
            401: error_response,
            404: error_response
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=cart_item_schema,
        responses={
            201: CartItemSerializer,
            400: error_response,
            401: error_response
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=cart_item_schema,
        responses={
            200: CartItemSerializer,
            400: error_response,
            401: error_response,
            404: error_response
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=cart_item_schema,
        responses={
            200: CartItemSerializer,
            400: error_response,
            401: error_response,
            404: error_response
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            204: 'No content',
            401: error_response,
            404: error_response
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)