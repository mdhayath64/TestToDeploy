from rest_framework.response import Response
from rest_framework.views import APIView

from core.service.user_subscription_service import UserSubscriptionService
from utility.api_framework import ApiFramework
from utility.common_utils import custom_response_obj


class UsersPlansView(APIView, ApiFramework):

    serializer=None
    def process(self):
        return UserSubscriptionService().plans_by_user(self.data)


    def get(self, request):
        self.data=request.GET.get('user_id', None)
        if request.user.is_superuser and self.data is None:
            resp=custom_response_obj(data=None, message='user_id is required', code=400)
            return Response(resp,400)
        elif not request.user.is_superuser:
            self.data=request.user.id
        return self.main()