from rest_framework.response import Response
from rest_framework.views import APIView

from e_commerce.users.service.user_service import UserService
from utility.api_framework import ApiFramework


class UpdateCompanyPortfolioView(APIView, ApiFramework):
    serializer=None
    __data=None
    def process(self):
        if self.method=="POST":
            return UserService().update_company_portfolio(self.__data)
        else:
            return UserService().get_company_portfolio()


    def post(self, request):
        user=request.user

        if not user.is_superuser:
            return Response(data={"message":"Unauthorized to perform this action"}, status=401)
        self.__data=request.data
        self.method="POST"
        self.__data['user']=user.id
        return self.main()

    def get(self, request):
        user = request.user
        self.method='GET'
        if not user.is_superuser:
            return Response(data={"message": "Unauthorized to perform this action"}, status=401)
        self.__data = request.data
        self.__data['user'] = user.id
        return self.main()