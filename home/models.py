from django.db import models
from django.conf import settings  # Reference the custom user model
from core.models import Product  # Import Product model

class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='wishlist_items'
    )  # Link to the custom user model
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='wishlisted_by'
    )  # Link to Product model
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the item was added

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlist entries

    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.product.name}"
