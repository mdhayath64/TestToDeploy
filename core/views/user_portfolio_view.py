from kombu.asynchronous.http import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from core.service.user_portfolio_service import PortfolioService
from middlewares.admin_permission import StrictOnlyAdmin
from utility.api_framework import ApiFramework
from utility.common_utils import custom_response_obj


class UserPortfolioServiceView(APIView, ApiFramework, PageNumberPagination):
    serializer=None
    permission_classes = [StrictOnlyAdmin]

    def process(self):
        investment_service=PortfolioService()
        if self.method=="POST":
            return investment_service.add_portfolio(self.data)
        elif self.method=="GET":
            return investment_service.get_portfolio(self.data,paginate=PageNumberPagination, request=self.request)
        elif self.method=="PUT":
            return investment_service.update_portfolio(self.data)
        elif self.method=="DELETE":
            return investment_service.delete_portfolio(self.data)


    def get(self, request):
        if not request.user.is_superuser:
            response=custom_response_obj(message="Unauthorized to perform this action", code=403)
            return Response(response, status=403)
        self.data=request.query_params
        self.method="GET"
        self.request=request
        return self.main()

    def post(self, request):
        self.data=request.data
        self.method="POST"
        return self.main()

    def put(self, request):
        self.data=request.data
        self.method="PUT"
        return self.main()

    def delete(self, request):
        self.data=request.GET.get("portfolio_mapping_id")
        if self.data is None:
            message=custom_response_obj(message="Please include portfolio_mapping_id in query param")
            return Response(data=message,status=400)
        self.method="DELETE"
        return self.main()
