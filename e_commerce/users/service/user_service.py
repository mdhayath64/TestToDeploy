import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from oauth2_provider.models import RefreshToken, Application, AccessToken
from django.utils import timezone
from oauthlib import common

from core.models import UserSubscriberMapping, UserPortfolio
from core.serializers.subscription_mapping_serializer import UserSubscriptionMappingSerializer
from core.serializers.subscription_serializer import SubscriptionSerializer
from core.serializers.user_detail_serializer import UserDetailsSerializer
from e_commerce.models import User, AdminCompanyPortfolio
from e_commerce.users.user_serializers.user_serializer import CreateUserSerializer, UpdateUserSerializer, \
    AdminPortfolioSerializer
from utility.common_utils import custom_response_obj
from utility.crud_helper import CrudHelper
from core.serializers.user_portfolio_mapping_serializer import UserPortfolioMappingDetailsSerializer
from datetime import timedelta

from utility.otp_manager import OTPManager
from utility.send_email_in_background import EmailSender


class UserService:

    __user_crud_helper=CrudHelper(CreateUserSerializer)
    __get_user_details=CrudHelper(UserSubscriptionMappingSerializer)

    """
        creates an obj in user field
    """
    def create_user(self, data):
        try:
            user = User.objects.get(phone=data.get('phone'))
            return custom_response_obj(data=CreateUserSerializer(user).data,code=400,message='User with this phone number already exists')
        except ObjectDoesNotExist:
            referral_code=data.get('referral_code', None)
            if referral_code is not None and len(referral_code)>0:
                user=User.objects.get(referral_code=referral_code)
                data['referred_by']=user.id
            data['referral_code']=uuid.uuid4().__str__()
            user=self.__user_crud_helper.add_obj(data)
            return user


    """
        get data by id , Id will always be primary key
        if id is not provided then return all data
    """
    def get_data(self, data, request=None, pagination=None):
        if data is not None:
            return self.__user_crud_helper.get_all_data(request=request, paginate=pagination, exclude={'email':request.user.email}, order_by_option='-subscription_payment_update')
        else:
            return self.__user_crud_helper.get_data_by_id(id=data.get('id'))
    """
        updates table obj using update data and primary key of the obj 
        that is currently being updated
    """
    def update_data(self, data, instance_primary_key):
        return CrudHelper(UpdateUserSerializer).update_obj(data, update_key_value=instance_primary_key)

    """
        Deletes data against the primary key
    """
    def delete_data(self, instance_primary_key):
        return self.__user_crud_helper.delete_obj(instance_primary_key)


    """
        Authenticate user and generate access token
    """
    def login_user(self, data):
        username = get_user_model().objects.get(phone=data.get('phone'))
        correct_password = username.check_password(data.get('password'))
        if correct_password:
            return self.__generate_token(username, data=data)
        else:
            return custom_response_obj(data=None, message='Invalid credentials, Please check your username/password',
                                       code=401)

    def __generate_token(self, user, data):
        application = Application.objects.all().first()

        remember_me = data.get('remember_me')
        if not remember_me:
            expires = timezone.now() + timedelta(seconds=18600)
        else:
            expires = timezone.now() + timedelta(days=30)
        current_token = common.generate_token()
        refresh_token = common.generate_token()
        access_token = AccessToken(
            user=user,
            scope='',
            expires=expires,
            token=current_token,
            application=application
        )
        access_token.save()
        refresh_token_data = RefreshToken(
            user=user,
            token=refresh_token,
            application=application,
            access_token=access_token
        )
        refresh_token_data.save()
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return custom_response_obj(data={
            'access_token': current_token,
            'refresh_token': refresh_token,
            'expiry': expires,
            'user': user.username,
            'email':user.email,
            'subscription_done':user.subscription_done,
            },

            code=200)
    """
        Refresh access token
    """
    def refresh_token(self, data):
        refresh_token = self.__validate_refresh_token(refresh_token=data['refresh_token'])
        if refresh_token is not None:
            user = refresh_token.user
            refresh_token.revoked = timezone.now()
            refresh_token.save()
            return self.__generate_token(user=user, data=data)
        else:
            return custom_response_obj(data=None,
                                       message='Invalid refresh token, please login to generate new access token',
                                       )

    def __validate_refresh_token(self, refresh_token):
        try:
            refresh_token=RefreshToken.objects.get(token=refresh_token,revoked__isnull=True)
            return refresh_token
        except ObjectDoesNotExist:
            return None


    def list_all_users(self, options):
        filter_options=["username","phone","email"]
        filters={}
        for i in filter_options:
            value=options.get(i, None)
            if value:
                filters[i]=value


        users=self.__user_crud_helper.get_all_data(filters)
        return users



    def get_user_details(self, user_id):
        try:
            user=User.objects.get(id=user_id)

            subscriptions_taken=UserSubscriberMapping.objects.filter(user__id=user.id)
            portfolio=UserPortfolio.objects.filter(user__id=user.id)
            user_sub=[]
            for i in subscriptions_taken:
                sub_taken=i.subscription_plan
                user_sub.append({
                "plan_id": sub_taken.plan_id,
                "created_at": sub_taken.created_at,
                "updated_at":sub_taken.updated_at,
                "name": sub_taken.name,
                "category": sub_taken.category,
                "description": sub_taken.category,
                "price": sub_taken.price,
                "term": sub_taken.term,
                "re_payment_type": sub_taken.re_payment_type,
                "sub_icon": sub_taken.sub_icon,
                "expected_return": sub_taken.expected_return,
                "is_active":i.is_active,
                "priority": sub_taken.priority,
                "user_subscriber_id":i.user_subscriber_id,
                "amount_paid":i.amount,
                "amount_activation_pending":i.amount_activation_pending
            })
            response={
                'user':UserDetailsSerializer(user).data,
                'subscriptions_taken':user_sub,
                'portfolio':UserPortfolioMappingDetailsSerializer(portfolio, many=True).data
            }
            return custom_response_obj(response, code=200)
        except ObjectDoesNotExist:
            return custom_response_obj(message=f'User details not found with id {user_id}',code=404)



    def request_otp(self,email, check_user=True):
        if check_user:
            try:
                User.objects.get(email=email)
            except ObjectDoesNotExist:
                return custom_response_obj(message='User not found in database', code=401)
        success, message = OTPManager.generate_and_send_otp(email, "Dear Customer")

        if success:
            return custom_response_obj(data={'response':'Otp sent successfully to your email'}, code=200)
        else:
            return custom_response_obj(message='Failed to send otp', code=500)

    def verify_otp(self,otp, email):
        success, message = OTPManager.verify_otp(email, otp)
        if success:
            return custom_response_obj(message='Otp verified successfully', code=200)
        else:
            return custom_response_obj(message=message, code=401)

    def reset_password(self,email, otp, password):
        success, message = OTPManager.verify_otp(email, otp)

        if success:
            user=User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return custom_response_obj(data={'response':'password reset successfully'})
        else:
            return custom_response_obj(message=message, code=401)

    def verify_user_registration(self , email, otp):
        success, message = OTPManager.verify_otp(email, otp)

        if success:
            return custom_response_obj(data={'response': 'user verified successfully'})
        else:
            return custom_response_obj(message=message, code=401)


    def update_company_portfolio(self, data):
        try:
            instance=AdminCompanyPortfolio.objects.get(user__id=data['user'])
            print("here")
            ser=AdminPortfolioSerializer(instance=instance,data=data, partial=True)
        except:
            ser=AdminPortfolioSerializer(data=data)
        print(data)
        if ser.is_valid():
            ser.save()
            return custom_response_obj(data={'response':ser.data},code=200)
        else:
            return custom_response_obj(message=ser.errors.__str__(),code=400)


    def get_company_portfolio(self):

        instance=AdminCompanyPortfolio.objects.all()
        ser=AdminPortfolioSerializer(instance, many=True)
        return custom_response_obj(data=ser.data,code=200)

