
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('profile/', views.profile, name='profile'),
    path('add_address/', views.add_address, name='add_address'),
    path('delete_address/<int:pk>/', views.delete_address, name='delete_address'),


    path(
        'accounts/password_reset/',
        auth_views.PasswordResetView.as_view(template_name='core/accounts/password_reset.html'),
        name='password_reset'
    ),
    path(
        'accounts/password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(template_name='core/accounts/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='core/accounts/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'accounts/reset_done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='core/accounts/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]
