from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
import razorpay
from django.contrib import messages


@login_required
def process_payment(request, order_id):
    """
    Handles the Razorpay payment process.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Ensure the order's total price is valid
    if order.total_price <= 0:
        return render(request, 'payment/error.html', {'message': 'Invalid order price.'})

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY_ID, settings.RAZORPAY_API_SECRET))

    try:
        # Create Razorpay order
        razorpay_order = client.order.create({
            "amount": int(order.total_price * 100),  # Amount in paise
            "currency": "INR",
            "payment_capture": "1",  # Auto-capture payment
        })
    except razorpay.errors.RazorpayError as e:
        return render(request, 'payment/error.html', {'message': f'Error creating Razorpay order: {str(e)}'})

    # Pass Razorpay details to the template
    return render(request, 'process_payment.html', {
        'order': order,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key': settings.RAZORPAY_API_KEY_ID,
    })


@login_required

def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.payment_status = 'Paid'  # Ensure this field exists in the model
    order.save()

    return render(request, 'payment/payment_success.html', {'order': order})

@login_required
def payment_failure(request, order_id):
    """
    Handles Razorpay payment failure.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Mark the order's payment status as failed
    order.payment_status = "Failed"
    order.save()

    return render(request, 'payment/failure.html', {"order": order})


from  core.models import Order
from payment. models import Payment

# Razorpay API client initialization
razorpay_client = razorpay.Client(auth=("your_key_id", "your_key_secret"))

@login_required
def order_confirmation(request, order_id):
    """
    Displays order confirmation and checks payment status for Razorpay orders.
    """
    order = get_object_or_404(Order, id=order_id)
    print("cod")

    if order.payment_method == 'Razorpay' and not order.is_paid:
        try:
            payment = Payment.objects.get(order=order)
            razorpay_payment = razorpay_client.payment.fetch(payment.payment_id)

            if razorpay_payment['status'] == 'captured':  # Check if payment is successful
                order.is_paid = True
                payment.payment_status = 'Succeeded'
                order.save()
                payment.save()
                messages.success(request, "Payment succeeded!")
            else:
                messages.warning(request, "Payment not completed. Please try again.")
        except Exception as e:
            messages.error(request, f"Error verifying payment status: {str(e)}")

    return render(request, 'order_confirmation.html', {'order': order})


import logging
logger = logging.getLogger(__name__)

@login_required
def orders(request):
    """
    Displays the list of orders for the logged-in user.
    """
    try:
        # Fetch orders for the logged-in user, sorted by newest first
        orders = Order.objects.filter(user=request.user).order_by('-created_at')

        # Debugging: Print orders
        logger.debug(f"Orders for user {request.user.username}: {orders}")

        # Add warning if no orders found
        if not orders.exists():
            messages.warning(request, "You don't have any orders yet.")

        return render(request, 'orders.html', {'orders': orders})

    except Exception as e:
        # Log the exception and display an error message
        logger.error(f"Error fetching orders: {str(e)}")
        messages.error(request, "An error occurred while fetching your orders. Please try again later.")
        return render(request, 'orders.html', {'orders': []})
