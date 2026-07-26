from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, F

from core.models import UserSubscriberMapping, UserPortfolio
from core.serializers.subscription_mapping_serializer import UserDetailsSubscriptionMappingSerializer
from utility.common_utils import custom_response_obj
from dateutil import parser as parser

class RaiseWithdrawalRequest:

    def raise_withdrawal(self, data):
        try:
            user_sub_mapping=UserSubscriberMapping.objects.get(user_subscriber_id=data['user_subscriber_id'],
                                                               withdraw_request_accepted=False,
                                                               is_active=True)
            term=user_sub_mapping.subscription_plan.term
            paid_on=parser.parse(str(user_sub_mapping.paid_on)).date()

            withdraw_release=(paid_on + timedelta(days=30 * int(term)))

            current_day=datetime.now().date()
            print("paid on", paid_on, current_day)
            if current_day>=withdraw_release:

                user_sub_mapping.wallet_id=data.get('wallet_id', user_sub_mapping.user.wallet_id)
                user_sub_mapping.withdraw_request_raised=True
                user_sub_mapping.withdraw_request_raised_on=datetime.now().date()
                user_sub_mapping.save()

                return custom_response_obj(data={'response':'withdrawal request saved'}, code=200)
            return custom_response_obj(data={'response': 'withdrawal request not allowed before term is over'}, code=200)
        except ObjectDoesNotExist:
            return custom_response_obj(message='requested details not found', code=404)

    def close_withdrawal_request(self, data):
        try:
            user_sub_mapping = UserSubscriberMapping.objects.get(user_subscriber_id=data['user_subscriber_id'],
                                                                 withdraw_request_raised=True,
                                                                 is_active=True)

            portfolio_total=UserPortfolio.objects.filter(user__id=user_sub_mapping.user.id,
                                                           subscription_plan__plan_id=user_sub_mapping.subscription_plan.plan_id,
                                                           amount_added_on__gte=user_sub_mapping.paid_on).aggregate(withdrawal_amount=Sum(F('amount'), default=0))

            amount_withdrwable=portfolio_total.get('withdrawal_amount',0)+user_sub_mapping.amount
            user_sub_mapping.withdraw_request_accepted = True
            user_sub_mapping.withdraw_request_raised=False
            user_sub_mapping.withdraw_request_raised_accepted_on = datetime.now().date()
            user_sub_mapping.paid=True
            user_sub_mapping.paid_on=datetime.now().date()
            user_sub_mapping.is_active=False
            user_sub_mapping.withdrawal_amount = amount_withdrwable
            user_sub_mapping.save()

            return custom_response_obj(data={'response': 'withdrawal request saved'}, code=200)
        except ObjectDoesNotExist:
            return custom_response_obj(message='requested details not found', code=404)


    def get_withdrawal_request(self):
        user_sub_mapping = UserSubscriberMapping.objects.filter(withdraw_request_raised=True, is_active=True)
        return custom_response_obj(data=UserDetailsSubscriptionMappingSerializer(user_sub_mapping, many=True).data)

