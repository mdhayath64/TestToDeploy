from click.core import batch
from django.utils.translation import gettext_lazy as _
import uuid
from django.db import models

from core.constants import Categories
from e_commerce.models import User

# Create your models here.
class Timestampedmodel(models.Model):
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified at"), auto_now=True)

    class Meta:
        abstract = True



class Address(Timestampedmodel):
    address_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_address"
    )
    building_name = models.CharField(max_length=1000, null=True, blank=True)
    address_line_1 = models.CharField(max_length=1000)
    address_line_2 = models.CharField(max_length=1000, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=100)
    latitude = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True
    )

    def __str__(self) -> str:
        return str(self.address_id)


class SubscriptionPlan(Timestampedmodel):
    plan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=100, unique=True)
    category=models.CharField(max_length=100, choices=[(e.value,e.value) for e in Categories], default=Categories.Stocks.value)
    description=models.TextField(max_length=2000, null=True, blank=True)
    price=models.FloatField()
    term=models.CharField(max_length=100, null=True, blank=True)
    re_payment_type=models.CharField(max_length=100, choices=[("MONTHLY","MONTHLY"),("WEEKLY","WEEKLY"),("END_OF_TERM","END_OF_TERM")], default="MONTHLY")
    sub_icon=models.CharField(max_length=1000, null=True, blank=True)
    expected_return=models.FloatField()
    is_exclusive=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)
    priority=models.IntegerField(default=2)

    def __str__(self):
        return str(self.name)



class UserSubscriberMapping(Timestampedmodel):
    user_subscriber_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribed_users')
    subscription_plan=models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subscribers_details')
    paid=models.BooleanField(default=False)
    paid_on=models.DateField(null=True, blank=True)
    next_payment_on=models.DateField(null=True, blank=True)
    is_active=models.BooleanField(default=False)
    last_payout_done=models.DateField(null=True, blank=True)
    withdraw_request_raised=models.BooleanField(default=False)
    withdraw_request_raised_on=models.DateField(null=True, blank=True)
    withdraw_request_accepted=models.BooleanField(default=False)
    withdraw_request_raised_accepted_on=models.DateField(null=True, blank=True)
    withdrawal_amount=models.FloatField(default=0.0)
    amount=models.FloatField(default=0.0)
    wallet_id=models.CharField(max_length=100, default='')
    amount_activation_pending=models.FloatField(default=0.0)

class UserPayouts(Timestampedmodel):
    user_payouts_id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_subs_map_id = models.ForeignKey(UserSubscriberMapping, on_delete=models.CASCADE,
                                         related_name='user_sub_payout')
    paid=models.BooleanField(default=False)
    paid_on=models.DateField(null=True, blank=True)
    payout_amount=models.FloatField()

    class Meta:
        unique_together = ('user_subs_map_id', 'created_at')


class ReferralPayouts(Timestampedmodel):
    referral_payout_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount=models.FloatField()
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='referral_payout')
    referred_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='referred_user')
    paid=models.BooleanField(default=False)



class UserPortfolio(Timestampedmodel):
    portfolio_mapping_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_portfolio')
    amount=models.FloatField()
    subscription_plan=models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='users_subscription')
    amount_added_on=models.DateField()


from django.db import models

class TrendingSymbol(models.Model):
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)  # crypto, stock, etc.
    exchange = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    change = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    market_cap = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    volume = models.BigIntegerField(null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'trending_symbols'

class AddSubscriptionBackground(Timestampedmodel):
    file_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_url=models.CharField(max_length=1000)
