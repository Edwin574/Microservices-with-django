# E-Commerce Microservices Platform

This project implements a modern e-commerce platform using a microservices architecture with Django and Django REST Framework. Each microservice is designed to be independently deployable while maintaining clear boundaries of responsibility.

## Project Structure

```
Microservices/
├── product_catalog/    # Product Management Service
│   ├── models.py      # Product data model
│   ├── serializers.py # Product data serialization
│   ├── views.py       # Product API endpoints
│   └── urls.py        # Product route definitions
├── shopping_cart/     # Shopping Cart Service
│   ├── models.py      # Cart and CartItem models
│   ├── serializers.py # Cart data serialization
│   ├── views.py       # Cart management endpoints
│   └── urls.py        # Cart route definitions
├── accounts/          # User Management Service
│   ├── models.py      # Custom User model
│   ├── serializers.py # User data serialization
│   ├── views.py       # User authentication endpoints
│   └── urls.py        # User route definitions
├── orders/            # Order Management Service
│   ├── models.py      # Order and OrderItem models
│   ├── serializers.py # Order data serialization
│   ├── views.py       # Order processing endpoints
│   └── urls.py        # Order route definitions
└── core/              # Shared Functionality
    └── utils.py       # Common utilities
```

## Microservices Overview

### 1. Product Catalog Service
- **Purpose**: Manages product information and inventory
- **Key Features**:
  - Product creation and management
  - Inventory tracking
  - Product search and filtering
- **Models**:
  - `Product`: Stores product details (name, description, price, stock)
- **Endpoints**:
  - GET `/api/products/`: List all products
  - POST `/api/products/`: Create new product (admin only)
  - GET `/api/products/{id}/`: Get product details
  - PUT/PATCH `/api/products/{id}/`: Update product (admin only)
  - DELETE `/api/products/{id}/`: Delete product (admin only)

### 2. Shopping Cart Service
- **Purpose**: Handles shopping cart operations
- **Key Features**:
  - Cart creation and management
  - Add/remove items
  - Update quantities
- **Models**:
  - `Cart`: User's shopping cart
  - `CartItem`: Items in cart with quantities
- **Endpoints**:
  - GET `/api/carts/`: Get user's cart
  - POST `/api/carts/add_item/`: Add item to cart
  - POST `/api/carts/remove_item/`: Remove item from cart
  - PUT `/api/carts/update_quantity/`: Update item quantity

### 3. User Management Service (Accounts)
- **Purpose**: Manages user accounts and authentication
- **Key Features**:
  - User registration and authentication
  - Profile management
  - Address management
- **Models**:
  - `Customer`: Extended user model with additional fields
- **Endpoints**:
  - POST `/api/accounts/register/`: Register new user
  - POST `/api/accounts/login/`: User login
  - GET `/api/accounts/profile/`: Get user profile
  - PUT `/api/accounts/profile/`: Update profile

### 4. Order Management Service
- **Purpose**: Handles order processing and management
- **Key Features**:
  - Order creation from cart
  - Order status management
  - Order history
- **Models**:
  - `Order`: Order details and status
  - `OrderItem`: Individual items in an order
- **Endpoints**:
  - POST `/api/orders/`: Create new order
  - GET `/api/orders/`: List user's orders
  - GET `/api/orders/{id}/`: Get order details
  - POST `/api/orders/{id}/cancel/`: Cancel order

## Service Communication

- Services communicate through RESTful APIs
- Each service maintains its own database tables
- Cross-service operations are handled through API calls

## Data Models

### Product Model
```python
class Product:
    name: str
    description: str
    price: Decimal
    stock: int
    created_at: DateTime
    updated_at: DateTime
```

### Cart Models
```python
class Cart:
    user: Customer
    created_at: DateTime
    updated_at: DateTime

class CartItem:
    cart: Cart
    product: Product
    quantity: int
```

### Customer Model
```python
class Customer(AbstractUser):
    phone_number: str
    address: str
```

### Order Models
```python
class Order:
    user: Customer
    status: str  # pending/processing/shipped/delivered/cancelled
    total_amount: Decimal
    shipping_address: str

class OrderItem:
    order: Order
    product: Product
    quantity: int
    price: Decimal
```

## Authentication and Security

- JWT-based authentication
- Role-based access control
- Admin-only endpoints for sensitive operations

## API Documentation

- Swagger/OpenAPI documentation available at `/api/docs/`
- Each endpoint includes:
  - Request/Response schemas
  - Authentication requirements
  - Example requests

## Development Setup

1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Run development server: `python manage.py runserver`

## Testing

Each microservice includes its own test suite:
- Unit tests for models and business logic
- Integration tests for API endpoints
- Run tests: `python manage.py test`


