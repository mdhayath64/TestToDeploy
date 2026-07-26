from rest_framework import serializers

from core.models import UserSubscriberMapping
from core.serializers.subscription_serializer import SubscriptionSerializer
from e_commerce.models import User


class UserSubscriptionMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserSubscriberMapping
        fields='__all__'


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username','phone','email']


class UserDetailsSubscriptionMappingSerializer(serializers.ModelSerializer):
    user=UserDetailsSerializer()
    subscription_plan=SubscriptionSerializer()

    class Meta:
        model=UserSubscriberMapping
        fields='__all__'