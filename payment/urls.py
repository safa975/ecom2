from django.urls import path
from . import views
from django.http import HttpResponse


app_name = 'payment'  # Set the app_name for this app

urlpatterns = [
    path('process-payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment-failure/<int:order_id>/', views.payment_failure, name='payment_failure'),
    path('orders/', views.orders, name='orders'),  # Correct URL pattern for orders view



]
