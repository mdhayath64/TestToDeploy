from rest_framework.views import APIView

from core.service.user_payouts import UserPayoutsDetails
from middlewares.admin_permission import StrictOnlyAdmin
from utility.api_framework import ApiFramework


class ReferralPayoutsView(APIView, ApiFramework):

    serializer=None

    permission_classes = [StrictOnlyAdmin]

    def process(self):
        service=UserPayoutsDetails()
        if self.method=='GET':
            return service.get_referral_payouts()
        elif self.method=='PATCH':
            return service.marked_referral_as_paid(self.data)
        elif self.method=="DELETE":
            return service.delete_refferral_payment(self.data)



    def patch(self, request):
        self.method = 'PATCH'
        self.data = request.GET.get('referral_payout_id')
        return self.main()

    def get(self, request):
        self.method='GET'
        return self.main()

    def delete(self, request):
        self.method="DELETE"
        self.data = request.GET.get('referral_payout_id')
        return self.main()