from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Product, Cart, OrderItem, Category, Order  # Add Order model here
from django.db.models import Q
from accounts.models import Address
from django.core.paginator import Paginator




@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    cart_data = []
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    for item in cart_items:
        subtotal = item.product.price * item.quantity
        cart_data.append({
            'id': item.id,
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': subtotal,
        })

    return render(request, 'core/cart.html', {
        'cart_items': cart_data,
        'total_price': total_price,
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.available_count <= 0:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect('core:product_detail', product_id=product.id)

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        if cart_item.quantity < product.available_count:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.error(request, f"Cannot add more of {product.name}. Only {product.available_count} in stock.")
            return redirect('core:product_detail', product_id=product.id)
    else:
        cart_item.quantity = 1
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart.")
    return redirect('core:cart')

@login_required
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))

        if 0 < new_quantity <= cart_item.product.available_count:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f"Quantity of {cart_item.product.name} updated to {new_quantity}.")
        else:
            messages.error(request, f"Invalid quantity for {cart_item.product.name}.")
    return redirect('core:cart')

@login_required
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")
    except Cart.DoesNotExist:
        messages.error(request, "Could not find the item in your cart.")
    return redirect('core:cart')
@login_required
def checkout(request):
    user_addresses = Address.objects.filter(user=request.user)  # Get user addresses

    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('core:cart')

    # Get the total price and discounted total
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    discounted_total = request.session.get('new_total', total_price)  # Use total_price if no discount applied

    print(f"Discounted Total in Session (checkout): {discounted_total}")

    if request.method == "POST":
        name = request.POST.get('name')
        address_id = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        postal_code = request.POST.get('zipcode')
        payment_method = request.POST.get('payment_method')

        if address_id:
            address = get_object_or_404(Address, id=address_id, user=request.user)
            street_address = address.street
            city = address.city
            state = address.state
            postal_code = address.zipcode
        else:
            street_address = request.POST.get('address')

        # Use the discounted total for the order
        order = Order.objects.create(
            user=request.user,
            name=name,
            address=street_address,
            city=city,
            country=country,
            postal_code=postal_code,
            total_price=discounted_total  # Save discounted total
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        print(payment_method)

        if payment_method == "cod":
            print("inside cod")
            cart_items.delete()
            return redirect('payment:order_confirmation', order_id=order.id)
        else:
            return redirect(reverse('payment:process_payment', args=[order.id]))

    return render(request, 'core/checkout.html', {
        'user_addresses': user_addresses,
        'cart_items': cart_items,
        'total_price': total_price,
        'discounted_total': discounted_total,  # Pass discounted total to the template
    })


from adminpanel.models import Banner

def index(request):
    # Fetch the active banner
    banner = Banner.objects.filter(active=True).first()

    featured_products_list = Product.objects.filter(is_featured=True).order_by('-created_at')
    paginator = Paginator(featured_products_list, 10)
    page_number = request.GET.get('page', 1)
    featured_products = paginator.get_page(page_number)

    categories = Category.objects.all().order_by('category_name')

    return render(request, 'core/index.html', {
        'banner': banner,
        'featured_products': featured_products,
        'categories': categories,
    })

def categories(request):
    categories = Category.objects.all().order_by('category_name')
    return render(request, 'core/categories.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products_list = category.product_set.all().order_by('name')
    paginator = Paginator(products_list, 10)
    page_number = request.GET.get('page', 1)
    products = paginator.get_page(page_number)

    return render(request, 'core/category_detail.html', {
        'category': category,
        'products': products,

    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'core/product_detail.html', {'product': product})

def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).order_by('name')

    return render(request, 'core/search.html', {
        'query': query,
        'results': results,
    })

def contact_us(request):
    return render(request, 'core/contact_us.html')

from .models import Coupon, Cart  # Ensure Cart and Coupon are correctly imported
from django.contrib import messages
from django.shortcuts import redirect

# Utility function to calculate the cart total
def calculate_cart_total(cart):
    try:
        # Calculate total by accessing the product's price and multiplying by quantity
        total = sum(item.product.price * item.quantity for item in cart)
    except (AttributeError, TypeError, ValueError) as e:
        print(f"Error calculating cart total: {e}")
        total = 0  # Default to 0 in case of error
    return total

# View to apply a coupon
def apply_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code', '').strip()
        cart = Cart.objects.filter(user=request.user)  # Fetch cart items for the user
        print("hello")
        print(f"Coupon Code: {coupon_code}")
        print(f"Cart: {cart}")

        if not cart.exists():  # Check if the cart is empty
            messages.error(request, "Your cart is empty.")
            print("Cart is empty.")
            return redirect('core:cart')

        # Calculate the total cart price
        total = calculate_cart_total(cart)
        print(f"Cart Total: {total}")

        try:
            # Find the coupon and validate it
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            print(f"Coupon Found: {coupon.code}")

            if not coupon.is_valid():  # Assuming `is_valid` is a method in the Coupon model
                messages.error(request, "This coupon is no longer valid.")
                print("Coupon is not valid.")
                return redirect('core:cart')

            # Calculate discount and new total
            discount_amount = (total * coupon.discount_amount) / 100
            discount_amount = min(discount_amount, total)  # Ensure discount doesn't exceed total
            new_total = total - discount_amount

            print(f"Discount Amount: {discount_amount}")
            print(f"New Total: {new_total}")

            # Store discount details in session
            request.session['discount'] = round(float(discount_amount), 2)
            request.session['new_total'] = round(float(new_total), 2)
            request.session['cart_total'] = round(float(new_total), 2)

            print(f"Discounted Total in Session: {request.session.get('new_total')}")


            messages.success(request, f"Coupon '{coupon_code}' applied successfully!")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid or expired coupon code.")
            print("Coupon does not exist.")
        except Exception as e:
            print(f"Unexpected Error: {e}")
            messages.error(request, "An unexpected error occurred. Please try again.")

    return redirect('core:cart')
