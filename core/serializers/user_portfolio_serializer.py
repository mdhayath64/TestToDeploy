from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.db import IntegrityError
from django.utils import timezone

from core.models import UserPayouts
from core.serializers.subscription_mapping_serializer import UserDetailsSubscriptionMappingSerializer


class UserPayoutSerializer(ModelSerializer):
    user_subs_map_id=UserDetailsSubscriptionMappingSerializer(many=False)
    class Meta:
        model=UserPayouts
        fields='__all__'


class UserPayoutDataSerializer(ModelSerializer):

    class Meta:
        model=UserPayouts
        fields='__all__'

    def validate(self, attrs):
        # Check if a UserPayouts with the same user_subs_map_id and created_on already exists
        created_on = attrs.get('created_at', timezone.now().date())
        user_subs_map_id = attrs.get('user_subs_map_id')

        if UserPayouts.objects.filter(user_subs_map_id=user_subs_map_id, created_at=created_on).exists():
            # Skip by raising a validation error, or handle it as needed
            raise serializers.ValidationError("A payout with this user_subs_map_id and created_on already exists.")

        return attrs

    def save(self, **kwargs):
        try:
            # Attempt to save the instance
            return super().save(**kwargs)
        except IntegrityError:
            # If unique constraint fails, handle it gracefully
            # Skip and return None, or implement logging as needed
            return None