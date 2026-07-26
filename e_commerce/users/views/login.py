from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from e_commerce.users.service.user_service import UserService
from utility.api_framework import ApiFramework


class LoginUserUtil(ApiFramework):

    def __init__(self, data, serializer_class=None, **kwargs):
        super().__init__(serializer_class=serializer_class)
        self.__data=data
        self.__response={}
        self.__service=UserService()
        self.__method=kwargs.get('method')
        self.__query_filters = {}

    def run_logic(self):
        self.__response=self.__service.login_user(self.__data)

    def process(self):
        return self.__response


class LoginUserView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        data=request.data
        return LoginUserUtil(data=data, method='POST').main()

