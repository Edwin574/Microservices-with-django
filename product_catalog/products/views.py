from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        product = self.get_object()
        stock_change = request.data.get('stock_change', 0)
        
        try:
            stock_change = int(stock_change)
            product.stock += stock_change
            if product.stock < 0:
                return Response(
                    {'error': 'Stock cannot be negative'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            product.save()
            return Response(ProductSerializer(product).data)
        except ValueError:
            return Response(
                {'error': 'Invalid stock change value'},
                status=status.HTTP_400_BAD_REQUEST
            ) 