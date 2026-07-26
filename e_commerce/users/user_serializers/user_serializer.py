from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from e_commerce.models import User, AdminCompanyPortfolio
from utility.utils import generate_referral_code


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        extra_kwargs={
            'password':{'write_only':True},
            'groups':{'write_only':True},
            'user_permissions':{'write_only':True}
        }

    def save(self):
        try:
            user=User.objects.get(phone=self.validated_data.get('phone'))
            return user
        except ObjectDoesNotExist:
            user = User(**self.validated_data)
            user.set_password(self.validated_data.get('password'))
            user.referral_code=generate_referral_code(length=10)
            user.save()
            return user



class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email','username','subscription_done','phone']
        extra_kwargs={
            'phone':{'read_only':True}
        }


class AdminPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminCompanyPortfolio
        fields='__all__'





