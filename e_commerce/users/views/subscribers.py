# from rest_framework.permissions import AllowAny
# from rest_framework.views import APIView
# from e_commerce.users.service.subscriber_service import SubscriberService
# from middlewares.custom_permission import AccountPermission
# from utility.api_framework import ApiFramework
#
#
# class SubscribeUserUtil(ApiFramework):
#
#     def __init__(self, data, serializer_class=None, **kwargs):
#         super().__init__(serializer_class=serializer_class)
#         self.__data = data
#         self.__response = {}
#         self.__service = SubscriberService()
#         self.__method = kwargs.get('method')
#         self.__query_filters = {}
#
#     def format_request(self):
#         if self.__method == 'GET':
#             for key, value in self.__data.items():
#                 self.__query_filters[key] = self.__data.get(key)
#
#     def run_logic(self):
#         if self.__method == 'POST':
#             self.__response = self.__service.add_subscribers(data=self.__data)
#         elif self.__method=='PATCH':
#             self.__response=self.__service.update_data(data=self.__data, instance_primary_key=self.__data.get('user_id'))
#         elif self.__method=='GET':
#             self.__response=self.__service.get_subscribers(filters_asked=self.__data)
#         else:
#             self.__response=self.__service.delete_data(id=self.__data.get('user'))
#
#     def process(self):
#         return self.__response
#
#
# class SubscriberView(APIView):
#
#     permission_classes = [AccountPermission(group_name='vendors')]
#     def post(self, request):
#         data = request.data.copy()
#         data['user']=request.user.user_id
#         return SubscribeUserUtil(data=data, method='POST').main()
#
#
#     def get(self, request):
#         query_options={'user__user_id':str(request.user.user_id) }
#         return SubscribeUserUtil(data=query_options, method='GET').main()
#
#     def patch(self, request):
#         data = request.data
#         subscriber_id=request.user.subscribers.all().first()
#         data['subscriber_id']=subscriber_id.subscriber_id if subscriber_id is not None else subscriber_id
#         return SubscribeUserUtil(data=data, method='PATCH').main()
