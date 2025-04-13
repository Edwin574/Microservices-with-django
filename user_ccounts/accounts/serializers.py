from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Customer, PasswordResetToken, EmailVerificationToken
import uuid
from datetime import timedelta
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'date_of_birth', 'gender',
            'address', 'city', 'state', 'country', 'postal_code',
            'is_verified', 'newsletter_subscription', 'marketing_emails',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_verified']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'phone_number',
            'date_of_birth', 'gender', 'address', 'city',
            'state', 'country', 'postal_code',
            'newsletter_subscription', 'marketing_emails'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = Customer.objects.create_user(**validated_data)
        
        # Create email verification token
        token = str(uuid.uuid4())
        EmailVerificationToken.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(days=1)
        )
        
        # TODO: Send verification email
        return user

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        
        try:
            reset_token = PasswordResetToken.objects.get(
                token=attrs['token'],
                is_used=False,
                expires_at__gt=timezone.now()
            )
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({"token": "Invalid or expired token."})
        
        attrs['reset_token'] = reset_token
        return attrs

class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            verification_token = EmailVerificationToken.objects.get(
                token=attrs['token'],
                is_used=False,
                expires_at__gt=timezone.now()
            )
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError({"token": "Invalid or expired token."})
        
        attrs['verification_token'] = verification_token
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_verified'] = user.is_verified
        token['is_active'] = user.is_active
        
        return token 