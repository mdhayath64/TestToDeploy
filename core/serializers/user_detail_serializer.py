from rest_framework import serializers

from core.models import ReferralPayouts
from e_commerce.models import User


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['id','email','phone','username','referral_code',"wallet_id"]



class ReferralPayoutSerializer(serializers.ModelSerializer):
    user=UserDetailsSerializer(many=False)
    referred_user=UserDetailsSerializer(many=False)
    class Meta:
        model=ReferralPayouts
        fields='__all__'
