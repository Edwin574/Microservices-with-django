from drf_yasg import openapi

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
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
        'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Date of birth'),
        'gender': openapi.Schema(type=openapi.TYPE_STRING, enum=['M', 'F', 'O'], description='Gender'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address'),
        'city': openapi.Schema(type=openapi.TYPE_STRING, description='City'),
        'state': openapi.Schema(type=openapi.TYPE_STRING, description='State'),
        'country': openapi.Schema(type=openapi.TYPE_STRING, description='Country'),
        'postal_code': openapi.Schema(type=openapi.TYPE_STRING, description='Postal code'),
        'newsletter_subscription': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Subscribe to newsletter'),
        'marketing_emails': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Allow marketing emails'),
    },
)

register_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
        'user': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
                'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Date of birth'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, enum=['M', 'F', 'O'], description='Gender'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address'),
                'city': openapi.Schema(type=openapi.TYPE_STRING, description='City'),
                'state': openapi.Schema(type=openapi.TYPE_STRING, description='State'),
                'country': openapi.Schema(type=openapi.TYPE_STRING, description='Country'),
                'postal_code': openapi.Schema(type=openapi.TYPE_STRING, description='Postal code'),
                'is_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Email verification status'),
                'newsletter_subscription': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Newsletter subscription status'),
                'marketing_emails': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Marketing emails status'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Account creation date'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Last update date'),
            },
        ),
    },
)

password_reset_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['email'],
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
    },
)

password_reset_confirm = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['token', 'new_password', 'new_password2'],
    properties={
        'token': openapi.Schema(type=openapi.TYPE_STRING, description='Password reset token'),
        'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password'),
        'new_password2': openapi.Schema(type=openapi.TYPE_STRING, description='New password confirmation'),
    },
) 