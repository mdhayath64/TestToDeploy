from rest_framework import serializers

from core.models import SubscriptionPlan, AddSubscriptionBackground


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model=SubscriptionPlan
        fields='__all__'



class AddSubscriptionBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model=AddSubscriptionBackground
        fields='__all__'