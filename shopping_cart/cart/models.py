from django.db import models
from django.core.validators import MinValueValidator

class Cart(models.Model):
    user_id = models.CharField(max_length=100)  # External user ID from the user service
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
        ]

    def __str__(self):
        return f"Cart {self.id} - User {self.user_id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100)  # External product ID from the product service
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product_id')
        indexes = [
            models.Index(fields=['product_id']),
        ]

    def __str__(self):
        return f"CartItem {self.id} - Product {self.product_id} (Qty: {self.quantity})"

    @property
    def total_price(self):
        return self.quantity * self.unit_price
