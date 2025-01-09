from django.contrib import admin
from .models import Customer, Category, Product, Cart, Order, OrderItem,Coupon

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at', 'updated_at')
    inlines = [OrderItemInline]

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)


from django.contrib import admin
from .models import Coupon

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_amount', 'is_active', 'expires_at', 'created_at', 'is_valid_status')
    list_filter = ('is_active', 'expires_at', 'created_at')
    search_fields = ('code',)
    ordering = ('-created_at',)

    def is_valid_status(self, obj):
        """Display whether the coupon is valid in the admin."""
        return obj.is_valid()
    is_valid_status.short_description = 'Is Valid'  # Column header
    is_valid_status.boolean = True  # Show as a boolean indicator

admin.site.register(Coupon, CouponAdmin)
