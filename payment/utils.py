import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY_ID, settings.RAZORPAY_API_SECRET))

def create_order(amount, currency='INR', receipt='order_rcptid_11'):
    data = {
        "amount": amount * 100,  # Razorpay takes amount in paisa
        "currency": currency,
        "receipt": receipt,
        "payment_capture": 1
    }
    return client.order.create(data)
