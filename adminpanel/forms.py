from django import forms
from core.models import Category, Product,Coupon

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [ 'category_name','image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image']



from django import forms
from .models import Banner

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'description', 'image','active']  # List your actual fields here

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_amount','expires_at' ,'is_active','created_at']


