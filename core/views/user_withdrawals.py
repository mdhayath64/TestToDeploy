from rest_framework.views import APIView

from core.service.user_withdrawal import RaiseWithdrawalRequest
from utility.api_framework import ApiFramework


class UserWithdrawalView(APIView, ApiFramework):

    serializer=None

    def process(self):
        service=RaiseWithdrawalRequest()
        if self.method=='GET':
            return service.get_withdrawal_request()
        elif self.method=='POST':
            return service.raise_withdrawal(self.data)
        elif self.method=='PATCH':
            return service.close_withdrawal_request(data=self.data)

    def post(self, request):
        self.method='POST'
        self.data=request.data
        return self.main()

    def patch(self, request):
        self.method = 'PATCH'
        self.data = request.data
        return self.main()

    def get(self, request):
        self.method='GET'
        return self.main()
