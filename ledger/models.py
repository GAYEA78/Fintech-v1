from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone
from django.conf import settings

class OtpCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 300  # 5 min
    @staticmethod
    def generate_for(user):
        code = f"{random.randint(0, 999999):06d}"
        otp = OtpCode.objects.create(user=user, code=code)
        return otp

class KycDocument(models.Model):
    PENDING = 'P'; APPROVED = 'A'; REJECTED = 'R'
    STATUS_CHOICES = [(PENDING,'Pending'),(APPROVED,'Approved'),(REJECTED,'Rejected')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.FileField(upload_to='kyc/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"KYC for {self.user.username}: {self.get_status_display()}"


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Account"

class Transaction(models.Model):
    CREDIT = 'CR'
    DEBIT = 'DB'
    TRANSACTION_TYPES = [
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=2, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} of {self.amount} on {self.timestamp.strftime('%Y-%m-%d')}"
