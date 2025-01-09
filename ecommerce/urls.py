from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),        # Core app (homepage)
    path('accounts/', include('accounts.urls')),  # Accounts app
    path('adminpanel/', include('adminpanel.urls')),  # Admin panel app
    path('home/', include('home.urls')),  # Include home app URLs for wishlist
    path('checkout/', include('core.urls')),  # This includes the 'checkout' URL from 'core/urls.py'
    path('payment/', include('payment.urls', namespace='payment')),  # Ensure 'payment/urls.py' has app_name = 'payment'


]
