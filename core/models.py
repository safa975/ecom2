from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal
from accounts.models import CustomUser  # External dependency

# Customer Model
class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_field = PhoneNumberField()

    def __str__(self):
        return self.user.username

# Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, default='default/category.jpg')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def update_stock(self, quantity):
        if self.available_count >= quantity:
            self.available_count -= quantity
            self.save()
        else:
            raise ValueError("Insufficient stock")

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)

    def get_total_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        self.total_price = self.get_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

# Order Model
STATUS_CHOICES = [
    ('P', 'Pending'),
    ('C', 'Completed'),
    ('F', 'Failed'),
    ('D', 'Delivered'),
]

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='Unknown')
    address = models.CharField(max_length=255, default='Unknown')
    city = models.CharField(max_length=255, default='Unknown')
    country = models.CharField(max_length=100, default='Unknown')
    postal_code = models.CharField(max_length=20, default='Unknown')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='C')
    payment_method = models.CharField(max_length=50, default='COD')

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.get_status_display()}"

# OrderItem Model
class OrderItem(models.Model):
    order = models.ForeignKey('core.Order', on_delete=models.CASCADE, related_name="items")  # Use string reference
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)  # Use string reference
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"

# CartItem Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) in Cart"

    @property
    def subtotal(self):
        return self.product.price * self.quantity

from django.utils import timezone

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code

    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True
