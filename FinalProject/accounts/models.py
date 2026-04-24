from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class User(AbstractUser):
    pass # Uses Django's default fields: username, email, password

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default='PHP')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            # Generate a random 10-digit account number
            self.account_number = str(random.randint(1000000000, 9999999999))
        super().save(*args, **kwargs)

class Transaction(models.Model):
    TYPES = (('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ('transfer', 'Transfer'))
    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)
    destination_account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=20, choices=TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)