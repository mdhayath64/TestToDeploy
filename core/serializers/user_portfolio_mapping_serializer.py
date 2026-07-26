from rest_framework import serializers

from core.models import UserPortfolio
from core.serializers.subscription_serializer import SubscriptionSerializer
from e_commerce.users.user_serializers.user_serializer import UpdateUserSerializer


class UserPortfolioMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserPortfolio
        fields='__all__'



class UserPortfolioMappingDetailsSerializer(serializers.ModelSerializer):
    subscription_plan=SubscriptionSerializer(many=False)
    user=UpdateUserSerializer(many=False)

    class Meta:
        model = UserPortfolio
        fields = '__all__'