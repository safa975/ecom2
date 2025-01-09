# payment/models.py

from django.db import models

class Payment(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)  
    payment_status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # Use string reference for the foreign key to avoid circular import
    order = models.ForeignKey('core.Order', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"
    

