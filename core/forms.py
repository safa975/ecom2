from django import forms
from .models import Product  # Import the Product model from core

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'available_count', 'image', 'is_featured']


