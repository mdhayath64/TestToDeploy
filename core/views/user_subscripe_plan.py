from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from core.service.user_subscription_service import UserSubscriptionService
from utility.api_framework import ApiFramework
from utility.common_utils import custom_response_obj


class UserSubscriptionView(APIView, ApiFramework, PageNumberPagination):

    serializer=None

    def process(self):
        service=UserSubscriptionService()
        if self.method=="GET":
            return service.get_users_based_on_subscription(self.data, request=self.request, pagination=PageNumberPagination)

        elif self.method=="POST":
            return service.create_mapping(self.data)

        elif self.method=='PATCH':
            return service.update_sub_mapping(mapping_id=self.data.get('user_subscriber_id'),
                                              data_to_update=self.data)

    def get(self, request):
        self.method="GET"
        self.request=request
        self.data=request.GET.get("subscription_plan_id")
        if self.data is None:
            data=custom_response_obj(message='subscription_plan_id is required', code=400)
            return Response(data, 400)
        return self.main()

    def post(self, request):
        self.data=request.data
        self.data['user']=request.user.id
        self.method="POST"
        return self.main()


    def patch(self,request):
        self.data=request.data
        self.method='PATCH'
        return self.main()