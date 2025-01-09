from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from core.models import Product, Category
from core.forms import ProductForm
from django.http import JsonResponse
from django.db.models import Count



# Get the Custom User model
User = get_user_model()

# Function to check if the user is an admin
def admin_required(user):
    return user.is_superuser  # Ensures that only superuser/admin can access this view

# Ensure user is logged in and is an admin
@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    return render(request, 'admindashboard.html')

# List all users
@login_required
@user_passes_test(admin_required)
def user_management(request):
    users = User.objects.all()
    return render(request, 'usermanagement.html', {'users': users})

# Activate a user
@login_required
@user_passes_test(admin_required)
def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, 'Cannot modify superuser status.')
        return redirect('adminpanel:usermanagement')
    user.is_active = True
    user.save()
    messages.success(request, f'{user.username} has been activated.')
    return redirect('adminpanel:usermanagement')

# Deactivate a user
@login_required
@user_passes_test(admin_required)
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, 'Cannot modify superuser status.')
        return redirect('adminpanel:usermanagement')
    user.is_active = False
    user.save()
    messages.success(request, f'{user.username} has been deactivated.')
    return redirect('adminpanel:usermanagement')

# Logout view (redirecting to admin dashboard for now)
@login_required
@user_passes_test(admin_required)
def logout_view(request):
    logout(request)
    return redirect('core:login')  # Redirect to the login page or any desired page

# Product dashboard to list all products
@login_required
@user_passes_test(admin_required)
def product_dashboard(request):
    products = Product.objects.all()
    return render(request, 'productdashboard.html', {'products': products})

# Add a new product
@login_required
@user_passes_test(admin_required)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()  # Save the new product
            messages.success(request, 'Product added successfully!')
            return redirect('adminpanel:product_dashboard')  # Redirect to product dashboard
        else:
            messages.error(request, 'Error adding product. Please try again.')
    else:
        form = ProductForm()  # Create an empty form for GET requests
    return render(request, 'addproduct.html', {'form': form})

# Edit an existing product
@login_required
@user_passes_test(admin_required)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # Bind the form to the product instance
        if form.is_valid():
            form.save()  # Save the updated product
            messages.success(request, 'Product updated successfully!')
            return redirect('adminpanel:product_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'editproduct.html', {'form': form, 'product': product})

# Delete a product
@login_required
@user_passes_test(admin_required)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('adminpanel:product_dashboard')
    return render(request, 'deleteproduct.html', {'product': product})

# User profile view
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

# Edit user profile
@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # Validate username
        if username and username != user.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken.')
                return redirect('adminpanel:edit_profile')
        
        # Validate email
        if email and email != user.email:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Invalid email format.')
                return redirect('adminpanel:edit_profile')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already taken.')
                return redirect('adminpanel:edit_profile')

        # Save changes
        user.username = username
        user.email = email
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('adminpanel:profile')
    
    return render(request, 'editprofile.html', {'user': user})

# List all categories
@login_required
@user_passes_test(admin_required)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categorylist.html', {'categories': categories})

# Add a new category
@login_required
@user_passes_test(admin_required)
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_image = request.FILES.get('category_image')  # Get uploaded image file
        if not category_name:
            messages.error(request, 'Category name is required.')
            return redirect('adminpanel:add_category')
        if category_image and not category_image.content_type.startswith('image/'):
            messages.error(request, 'Only image files are allowed.')
            return redirect('adminpanel:add_category')
        Category.objects.create(
            category_name=category_name,
            category_image=category_image
        )
        messages.success(request, 'Category added successfully.')
        return redirect('adminpanel:category_list')
    return render(request, 'addcategory.html')

# Edit an existing category
@login_required
@user_passes_test(admin_required)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_image = request.FILES.get('category_image')
        
        # Validate category name and image
        if category_name:
            category.category_name = category_name
        if category_image:
            if not category_image.content_type.startswith('image/'):
                messages.error(request, 'Only image files are allowed.')
                return redirect('adminpanel:category_edit', pk=pk)
            category.category_image = category_image
        category.save()
        messages.success(request, 'Category updated successfully.')
        return redirect('adminpanel:category_list')
    return render(request, 'categoryedit.html', {'category': category})

# Delete a category
@login_required
@user_passes_test(admin_required)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('adminpanel:category_list')
    return render(request, 'deletecategory.html', {'category': category})

from django.http import JsonResponse
from django.db.models import Count
from core.models import Product, Category, Order  # Correct the model name here
from django.contrib.auth import get_user_model

User = get_user_model()

def get_dashboard_data(request):
    # Get the total count of users
    total_users = User.objects.count()

    # Get the total count of products
    total_products = Product.objects.count()

    # Get the total count of orders (using Order model)
    total_orders = Order.objects.count()

    # Get the total count of categories
    total_categories = Category.objects.count()

    # Example data for user growth (replace with actual data)
    user_growth = [10, 20, 30, 40, 50]  # Replace with real data if available

    # Example data for product sales (replace with actual sales data)
    product_sales = [30, 70, 50, 90]  # Replace with real data if available
    product_names = ['Product A', 'Product B', 'Product C', 'Product D']

    # Prepare the data for the response
    data = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_categories': total_categories,
        'user_growth': user_growth,
        'user_growth_labels': ['January', 'February', 'March', 'April', 'May'],
        'product_sales': product_sales,
        'product_names': product_names
    }

    return JsonResponse(data)

from core.models import Order


@login_required
@user_passes_test(admin_required)
def admin_order(request):
    """
    Display all orders in the admin panel.
    """
    orders = Order.objects.all() 
    return render(request, 'admin_order.html', {'orders': orders})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Banner
from .forms import BannerForm
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(admin_required)
def banner(request):
    banners = Banner.objects.all()
    return render(request, 'banner.html', {'banners': banners})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Banner
from .forms import BannerForm

@user_passes_test(admin_required)
def edit_banner(request, banner_id):
    try:
        banner = Banner.objects.get(id=banner_id)
    except Banner.DoesNotExist:
        # Redirect or show a message if the banner does not exist
        messages.error(request, "Banner not found.")
        return redirect('adminpanel:banner')

    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:banner')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'edit_banner.html', {'form': form})

from core.models import Coupon
from .forms import CouponForm


@login_required
@user_passes_test(admin_required)
def coupon_list(request):
    coupons = Coupon.objects.all()  
    return render(request, 'coupon_list.html', {'coupons': coupons})

# Add Coupon view
@login_required
@user_passes_test(admin_required)
def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon added successfully!")
            return redirect('adminpanel:coupon_list')  # Redirect to the coupon list page
    else:
        form = CouponForm()

    return render(request, 'add_coupon.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def edit_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon updated successfully!")
            return redirect('adminpanel:coupon_list')  # Redirect to the coupon list page
    else:
        form = CouponForm(instance=coupon)

    return render(request, 'edit_coupon.html', {'form': form, 'coupon': coupon})

# Delete Coupon view
@login_required
@user_passes_test(admin_required)
def delete_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    messages.success(request, "Coupon deleted successfully!")
    return redirect('adminpanel:coupon_list')  

