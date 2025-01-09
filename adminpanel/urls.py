# adminpanel/urls.py
from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('user_management/', views.user_management, name='user_management'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('logout/', views.logout_view, name='logout'),
    path('productdashboard/', views.product_dashboard, name='product_dashboard'),
    path('productdashboard/add/', views.add_product, name='add_product'),
    path('productdashboard/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('productdashboard/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('categories/<int:id>/edit/', views.category_edit, name='category_edit'),
    path('get_dashboard_data/', views.get_dashboard_data, name='get_dashboard_data'),
    path('orders/',views.admin_order, name='admin_order'),
    path('edit_banner/<int:banner_id>/', views.edit_banner, name='edit_banner'),
    path('banner/', views.banner, name='banner'),  # Banner list URL
    path('coupons/', views.coupon_list, name='coupon_list'),
    path('add-coupon/', views.add_coupon, name='add_coupon'),
    path('edit-coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('delete-coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),
 
   
]