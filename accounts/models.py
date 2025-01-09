from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # Use this to reference AUTH_USER_MODEL


# OTP Model
class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    otp_code = models.CharField(max_length=6)  # Assuming a fixed-length OTP
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.username}"  # Ensures readability in the admin panel

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)  # Email is unique and required

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255, default='Unknown')  # Set a default value here
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.city}"    