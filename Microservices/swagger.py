from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="E-Commerce Microservices API",
        default_version='v1',
        description="API documentation for E-Commerce Microservices Platform",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Common response schemas
error_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
    },
)

success_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
    },
)

# Authentication schemas
login_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'password'],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
    },
)

login_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
    },
)

register_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'email', 'password', 'password2'],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        'password2': openapi.Schema(type=openapi.TYPE_STRING, description='Password confirmation'),
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address'),
    },
)

# Product schemas
product_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Product ID'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Product name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='Product description'),
        'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Product price'),
        'stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Available stock'),
    },
)

# Cart schemas
cart_item_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Cart item ID'),
        'product': product_schema,
        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity'),
    },
)

cart_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Cart ID'),
        'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
        'items': openapi.Schema(type=openapi.TYPE_ARRAY, items=cart_item_schema),
        'total': openapi.Schema(type=openapi.TYPE_NUMBER, description='Cart total'),
    },
)

# Order schemas
order_item_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Order item ID'),
        'product': product_schema,
        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity'),
        'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Price at time of order'),
    },
)

order_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Order ID'),
        'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Order status'),
        'total_amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Order total'),
        'shipping_address': openapi.Schema(type=openapi.TYPE_STRING, description='Shipping address'),
        'items': openapi.Schema(type=openapi.TYPE_ARRAY, items=order_item_schema),
    },
) 