import uuid

import pyotp
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    phone = models.CharField(max_length=100, unique=True)
    username=models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    user_consent = models.BooleanField(default=False)
    subscription_done = models.BooleanField(default=False)
    subscription_payment_update=models.DateTimeField(null=True, blank=True)
    referral_code = models.CharField(max_length=100, default='')
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='customer_referral', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    wallet_id=models.CharField(max_length=1000, default='')

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "email"]

    def __str__(self):
        return str(self.username)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['phone', 'email'], name='unique_user')
        ]


class AdminCompanyPortfolio(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='company_portfolio')
    invested=models.FloatField(default=0.0)
    change=models.FloatField(default=0.0)
    trade_performed=models.IntegerField(default=0)


class OTPRecord(models.Model):
    email = models.EmailField()
    otp_secret = models.CharField(max_length=32)  # Store the OTP secret
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        """Check if OTP is still valid (within 2 minutes and not verified)"""
        return not self.is_verified and timezone.now() <= self.expires_at

    def verify(self, otp_input):
        """Verify the provided OTP"""
        if not self.is_valid():
            return False

        # Create TOTP object with 2-minute validity

        totp = pyotp.TOTP(self.otp_secret, interval=600)

        # Verify OTP
        if totp.verify(otp_input):
            self.is_verified = True
            self.save()
            return True
        return False

    def get_otp(self):
        """Generate current OTP"""
        totp = pyotp.TOTP(self.otp_secret, interval=600)
        return totp.now()

    @classmethod
    def create_otp_record(cls, email):
        """Create or update OTP record with 2-minute validity"""
        # Generate new secret
        secret = pyotp.random_base32()

        # Calculate expiry time (2 minutes from now)
        expires_at = timezone.now() + timedelta(minutes=10)

        # Get or create OTP record
        otp_record, created = cls.objects.get_or_create(
            email=email,
            defaults={
                'otp_secret': secret,
                'expires_at': expires_at,
                'is_verified': False
            }
        )

        # If record exists, update it
        if not created:
            otp_record.otp_secret = secret
            otp_record.expires_at = expires_at
            otp_record.is_verified = False
            otp_record.save()

        return otp_record