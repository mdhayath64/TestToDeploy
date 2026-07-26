from rest_framework.response import Response
from rest_framework.views import APIView

from e_commerce.users.service.user_service import UserService
from utility.api_framework import ApiFramework
from utility.common_utils import custom_response_obj


class UserDetailsView(APIView, ApiFramework):

    serializer=None
    def process(self):
        return UserService().get_user_details(self.data)

    def get(self, request):
        self.data=request.GET.get('user_id', None)

        if request.user.is_superuser and self.data is None:
            return Response(data= custom_response_obj(message='User id is required', code=400), status=400)
        elif not request.user.is_superuser:
            self.data=request.user.id
        return self.main()