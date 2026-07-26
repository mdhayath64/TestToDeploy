from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Sum

from core.models import SubscriptionPlan, UserSubscriberMapping, UserPortfolio
from core.serializers.subscription_mapping_serializer import UserSubscriptionMappingSerializer, UserDetailsSubscriptionMappingSerializer as DetailsSerializer
from core.service.user_payouts import UserPayoutsDetails
from e_commerce.models import User
from utility.common_utils import custom_response_obj
from utility.crud_helper import CrudHelper


class UserSubscriptionService:

    __crud_helper=CrudHelper(UserSubscriptionMappingSerializer)

    def create_mapping(self, data):
        try:
            user=User.objects.get(id=data.get('user'))
            plan_details=SubscriptionPlan.objects.get(plan_id=data.get('subscription_plan'))
            user.wallet_id=data.get('wallet_id',data.get('walled_id',''))
            user.subscription_done=True
            user.subscription_payment_update=datetime.now()
            user.save()

            if plan_details.re_payment_type=="MONTHLY":
                data['next_payment_on']=datetime.now().date()+timedelta(days=30)
            elif plan_details.re_payment_type=='END_OF_TERM':

                if int(str(plan_details.term).replace("Months","").replace("months","").replace(" ",""))==6:
                    days=182
                else:
                    days=365
                data['next_payment_on'] = datetime.now().date() + timedelta(days=days)


            # user_sub_mapping=UserSubscriberMapping.objects.filter(user__id=user.id,
            #                                                       subscription_plan__plan_id=data.get('subscription_plan'),
            #                                                       is_active=True).first()

            amount=float(data['amount'])


            #if user_sub_mapping is None:
            data['amount'] = 0
            data['amount_activation_pending'] = amount

            if user.referred_by is not None:
                UserPayoutsDetails().create_payout_per_user(user=user.referred_by, referred_user=user,
                                                                amount=float(amount * 0.10))

            return self.__crud_helper.add_obj(data)
            # else:
            #     data['amount_activation_pending'] = amount
            #return self.__crud_helper.update_obj(data, user_sub_mapping.user_subscriber_id)
        except ObjectDoesNotExist:
            return custom_response_obj(message='data not found', code=404)

    def get_users_based_on_subscription(self, subscription_plan_id, pagination, request):
        data=CrudHelper(DetailsSerializer).get_all_data({'subscription_plan__plan_id':subscription_plan_id},paginate=pagination, request=request)
        data['data']=[x['user'] for x in data['data']]
        return data

    def plans_by_user(self, user):
        data=UserSubscriberMapping.objects.filter(user__id=user).values('user_subscriber_id','paid','paid_on','is_active','amount','withdrawal_amount').annotate(
            name=F('subscription_plan__name'),
            description=F('subscription_plan__description'),
            price=F('subscription_plan__price'),
            term=F('subscription_plan__term'),
            expected_return=F('subscription_plan__expected_return'),
            re_payment_type=F('subscription_plan__re_payment_type'),
            plan_id=F('subscription_plan__plan_id'),
        )

        for i in data:
            portfolio=None
            if i['paid_on'] is not  None:
                portfolio=UserPortfolio.objects.filter(user__id=user,
                                                       subscription_plan__plan_id=i['plan_id'],
                                                       amount_added_on__gte=i['paid_on']
                                                       ).aggregate(amount_total=Sum(F('amount'),default=0))
                #print(portfolio,i.get('amount',0))
            if portfolio is not None:
                i['portfolio_value']=portfolio.get('amount_total',0)+i.get('amount',0)
            else:
                i['portfolio_value']=i.get('amount',0)
        return custom_response_obj(data=data, message='request processed successfully',code=200)


    def update_sub_mapping(self, mapping_id, data_to_update):
        is_active=data_to_update.get('is_active',False)
        user_data = UserSubscriberMapping.objects.get(user_subscriber_id=mapping_id)
        if is_active:
            amount=data_to_update.get("amount",None)

            user_data.amount+=float(amount)
            user_data.amount_activation_pending=0
            user_data.paid=True
            user_data.save()
        return self.__crud_helper.update_obj(data_to_update, mapping_id)

