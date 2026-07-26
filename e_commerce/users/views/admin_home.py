from rest_framework.response import Response
from rest_framework.views import APIView

from e_commerce.users.service.admin_home import AdminHome
from utility.api_framework import ApiFramework
from utility.common_utils import custom_response_obj


class AdminHomeView(APIView, ApiFramework):

    serializer=None

    def process(self):
        return AdminHome().get_admin_home()


    def get(self, request):
        if not request.user.is_superuser:
            return Response(data=custom_response_obj(message='Unauthorized to perform this acount', code=403), status=403)
        return self.main()