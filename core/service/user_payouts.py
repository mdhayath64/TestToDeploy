from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, F

from core.models import UserPayouts, UserSubscriberMapping, UserPortfolio, ReferralPayouts
from core.serializers.user_detail_serializer import ReferralPayoutSerializer
from core.serializers.user_portfolio_serializer import UserPayoutSerializer, UserPayoutDataSerializer
from utility.common_utils import custom_response_obj


class UserPayoutsDetails:


    def create_user_payouts(self):
        current_day = datetime.now().date()
        users=UserSubscriberMapping.objects.filter(next_payment_on=datetime.now().date())
        payouts_data=[]
        for i in users:
             if i.subscription_plan.re_payment_type=="MONTHLY":
                 amount_added_at_gte=current_day-timedelta(days=30)
                 i.next_payment_date=current_day+timedelta(days=30)
             elif i.subscription_plan.re_payment_type=="WEEKLY":
                 amount_added_at_gte=current_day-timedelta(days=7)
                 i.next_payment_date = current_day + timedelta(days=7)
             elif i.subscription_plan.re_payment_type=="END_OF_TERM":
                 amount_added_at_gte=current_day-timedelta(days=365)
             print(amount_added_at_gte)

             i.save()
             amount=UserPortfolio.objects.filter(user__id=i.user.id,subscription_plan__plan_id=i.subscription_plan.plan_id,
                                                 amount_added_on__gte=amount_added_at_gte, amount_added_on__lte=current_day).aggregate(total_amount=Sum(F('amount')))['total_amount']
             print(amount)
             payouts_data.append({'user_subs_map_id':i.user_subscriber_id,
                                  'payout_amount':amount})

        data=UserPayoutDataSerializer(data=payouts_data, many=True)
        if data.is_valid():
            data.save()
        else:
            print(data.errors)


    def create_payout_per_user(self,user, referred_user, amount ):
        try:
            referred_user=ReferralPayouts.objects.get(user=user, referred_user=referred_user)
        except ObjectDoesNotExist:
            referred_user=ReferralPayouts(user=user, referred_user=referred_user, amount=amount)
            referred_user.save()

    def mark_user_paid(self, data):
        UserPayouts.objects.filter(user_payouts_id__in=data['user_payouts_ids']).update(paid=True, paid_on=datetime.now().date())
        return custom_response_obj(data={'response':'payout marked as paid'}, code=200)


    def get_user_payouts(self,):
        users_payout=UserPayouts.objects.all()
        data=UserPayoutSerializer(users_payout, many=True).data
        return custom_response_obj(data=data, code=200)


    def get_referral_payouts(self):
        users=ReferralPayouts.objects.filter(paid=False)
        result=ReferralPayoutSerializer(users, many=True).data
        return custom_response_obj(data=result, code=200)


    def marked_referral_as_paid(self, referral_id):
        users = ReferralPayouts.objects.get(referral_payout_id=referral_id)
        users.paid=True
        users.save()
        result = ReferralPayoutSerializer(users,many=False).data
        return custom_response_obj(data=result, code=200)


    def delete_refferral_payment(self, referral_id):
        users = ReferralPayouts.objects.get(referral_payout_id=referral_id)
        users.delete()
        return custom_response_obj(data={'response':'deleted record successfully'}, code=200)

