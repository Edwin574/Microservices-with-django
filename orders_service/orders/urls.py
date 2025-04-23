from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import OrderViewSet, OrderItemViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

orders_router = routers.NestedDefaultRouter(router, r'orders', lookup='order')
orders_router.register(r'items', OrderItemViewSet, basename='order-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(orders_router.urls)),
] 