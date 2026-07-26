from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView


from e_commerce.users.service.user_service import UserService
from utility.api_framework import ApiFramework
from utility.common_utils import custom_response_obj


class UserUtil(ApiFramework):

    def __init__(self, data, serializer_class=None, **kwargs):
        super().__init__(serializer_class=serializer_class)
        self.__data=data
        self.__response={}
        self.__service=UserService()
        self.__method=kwargs.get('method')
        self.__query_filters = {}
        self.request=kwargs.get('request')
        self.pagination=kwargs.get('pagination')


    def run_logic(self):
        if self.__method=='POST':
            self.__response=self.__service.create_user(data=self.__data)
        elif self.__method=='PATCH':
            self.__response=self.__service.update_data(data=self.__data, instance_primary_key=self.__data.get('user_id'))
        elif self.__method=='GET':
            self.__response=self.__service.get_data(data=self.__query_filters, request=self.request, pagination=self.pagination)
        else:
            self.__response=self.__service.delete_data(instance_primary_key=self.__data.get('user_id'))

    def process(self):
        return self.__response


class UserView(APIView, PageNumberPagination):
    permission_classes = [AllowAny,]

    def post(self, request):
        data=request.data
        return UserUtil(data=data, method='POST').main()

    def get(self, request):
        query_options=request.GET.get("user_id", None)
        user=request.user
        if user=='AnonymousUser' or not request.user.is_superuser:
            data=custom_response_obj(data=None,message='Unauthorized, Please login to perform this action', code=401)
            return Response(data,status=HTTP_401_UNAUTHORIZED)
        return UserUtil(data=query_options,method='GET', request=request, pagination=PageNumberPagination).main()

    def patch(self, request):
        data = request.data
        if request.user=='AnonymousUser':
            data=custom_response_obj(message='Unauthorized, Please login to perform this action', code=401)
            return Response(data, status=HTTP_401_UNAUTHORIZED)
        elif not request.user.is_superuser:
            data['user_id']=request.user.id
        print(data)
        return UserUtil(data=data,method='PATCH').main()

    def delete(self, request):
        if request.user=='AnonymousUser' or not request.user.is_superuser:
            data=custom_response_obj(message='Unauthorized, Please login to perform this action', code=401)
            return Response(data, status=HTTP_401_UNAUTHORIZED)
        data={'user_id':request.GET.get('user_id')}
        return UserUtil(data=data, method='DELETE').main()
