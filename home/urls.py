from django.urls import path
from . import views

app_name = 'home'  # This sets the namespace for the URLs

urlpatterns = [
    path('wishlist/', views.wishlist, name='wishlist'),  # View wishlist page
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # Add to wishlist
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),  # Remove from wishlist
]
