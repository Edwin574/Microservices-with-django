import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer
from Microservices.swagger import product_schema, error_response

logger = logging.getLogger(__name__)

class HomeView(APIView):
    """
    Product Catalog Home View
    
    This endpoint provides a welcome message from the product catalog microservice.
    """
    @swagger_auto_schema(
        operation_description="Get a welcome message from the product catalog service",
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Welcome message')
                    }
                )
            )
        }
    )
    def get(self, request):
        logger.info("Product catalog home accessed", extra={"request_path": request.path})  # Structured log
        return Response({"message": "Hello from product catalog!"})

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        responses={
            200: ProductSerializer(many=True),
            401: error_response
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            200: ProductSerializer,
            401: error_response,
            404: error_response
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=product_schema,
        responses={
            201: ProductSerializer,
            400: error_response,
            401: error_response
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=product_schema,
        responses={
            200: ProductSerializer,
            400: error_response,
            401: error_response,
            404: error_response
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=product_schema,
        responses={
            200: ProductSerializer,
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

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

#  Similarly for other views, log requests and any errors