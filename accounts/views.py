from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from .serializers import CustomerSerializer, CustomTokenObtainPairSerializer
from Microservices.swagger import (
    register_request, success_response, error_response,
    login_request, login_response
)

class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello from Django microservice!"})

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomerSerializer

    @swagger_auto_schema(
        request_body=register_request,
        responses={
            201: success_response,
            400: error_response
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        request_body=login_request,
        responses={
            200: login_response,
            401: error_response
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer

    @swagger_auto_schema(
        responses={
            200: CustomerSerializer,
            401: error_response
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CustomerSerializer,
        responses={
            200: CustomerSerializer,
            400: error_response,
            401: error_response
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CustomerSerializer,
        responses={
            200: CustomerSerializer,
            400: error_response,
            401: error_response
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

