from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Wishlist
from django.contrib.auth.decorators import login_required
from core.models import Product

@login_required
def add_to_wishlist(request, product_id):
    """
    Add a product to the user's wishlist.
    """
    product = get_object_or_404(Product, id=product_id)  # Ensure product exists or raise 404

    # Attempt to get or create a wishlist entry
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, "Product added to your wishlist.")  # Notify the user of success
    else:
        messages.info(request, "This product is already in your wishlist.")  # Notify if already exists

    return redirect('home:wishlist')  # Redirect to the wishlist page


@login_required
def remove_from_wishlist(request, product_id):
    """
    Remove a product from the user's wishlist.
    """
    wishlist_item = Wishlist.objects.filter(user=request.user, product_id=product_id).first()
    if wishlist_item:
        wishlist_item.delete()  # Remove the item
        messages.success(request, "Product removed from your wishlist.")  # Notify the user
    else:
        messages.error(request, "This product is not in your wishlist.")  # Error if not found

    return redirect('home:wishlist')  # Redirect back to the wishlist page


@login_required
def wishlist(request):
    """
    Display the user's wishlist.
    """
    wishlist_items = Wishlist.objects.filter(user=request.user)  # Fetch all wishlist items
    return render(request, 'home/wishlist.html', {'wishlist_items': wishlist_items})
