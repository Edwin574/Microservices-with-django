from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import uuid
from .models import PasswordResetToken, EmailVerificationToken
from .serializers import (
    UserSerializer, UserRegistrationSerializer, PasswordChangeSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    EmailVerificationSerializer, CustomTokenObtainPairSerializer
)

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create email verification token
            token = EmailVerificationToken.objects.create(
                user=user,
                token=str(uuid.uuid4()),
                expires_at=timezone.now() + timedelta(days=1)
            )
            # Send verification email
            send_mail(
                'Verify your email',
                f'Click the link to verify your email: {settings.FRONTEND_URL}/verify-email/{token.token}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response({
                'message': 'User registered successfully. Please check your email for verification.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]


    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            # Create password reset token
            token = PasswordResetToken.objects.create(
                user=user,
                token=str(uuid.uuid4()),
                expires_at=timezone.now() + timedelta(hours=1)
            )
            # Send reset email
            send_mail(
                'Reset your password',
                f'Click the link to reset your password: {settings.FRONTEND_URL}/reset-password/{token.token}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset email sent'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = PasswordResetToken.objects.get(token=serializer.validated_data['token'])
            if token.is_expired():
                return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
            token.user.set_password(serializer.validated_data['new_password'])
            token.user.save()
            token.delete()
            return Response({'message': 'Password reset successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationView(APIView):
    permission_classes = [permissions.AllowAny]


    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            token = EmailVerificationToken.objects.get(token=serializer.validated_data['token'])
            if token.is_expired():
                return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
            token.user.is_verified = True
            token.user.save()
            token.delete()
            return Response({'message': 'Email verified successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

  
    def post(self, request):
        if request.user.is_verified:
            return Response({'error': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)
        # Delete any existing verification tokens
        EmailVerificationToken.objects.filter(user=request.user).delete()
        # Create new verification token
        token = EmailVerificationToken.objects.create(
            user=request.user,
            token=str(uuid.uuid4()),
            expires_at=timezone.now() + timedelta(days=1)
        )
        # Send verification email
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: {settings.FRONTEND_URL}/verify-email/{token.token}',
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )
        return Response({'message': 'Verification email sent'})
