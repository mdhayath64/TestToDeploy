from rest_framework.views import APIView

from core.service.user_payouts import UserPayoutsDetails
from utility.api_framework import ApiFramework


class UserPayoutsView(APIView, ApiFramework):

    serializer=None

    def process(self):
        service=UserPayoutsDetails()
        if self.method=='GET':
            return service.get_user_payouts()
        elif self.method=='POST':
            return service.create_user_payouts()
        elif self.method=='PATCH':
            return service.mark_user_paid(self.data)

    # def post(self, request):
    #     self.method='POST'
    #     self.data=request.data
    #     return self.main()

    def patch(self, request):
        self.method = 'PATCH'
        self.data = request.data
        return self.main()

    def get(self, request):
        self.method='GET'
        return self.main()
