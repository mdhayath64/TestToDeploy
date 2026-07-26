# from rest_framework.views import APIView
# from e_commerce.users.service.address_service import AddressService
# from e_commerce.users.user_serializers.address_serializer import AddressSerializer
# from utility.api_framework import ApiFramework
#
#
# class AddressUtil(ApiFramework):
#
#     def __init__(self, data, serializer_class=None, **kwargs):
#         super().__init__(serializer_class=serializer_class)
#         self.__data = data
#         self.__response = {}
#         self.__service = AddressService()
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
#             self.__response = self.__service.add_address(data=self.__data)
#         elif self.__method == 'PATCH':
#             self.__response = self.__service.update_data(data=self.__data, instance_primary_key=self.__data
#                                                          .get('address_id'))
#         elif self.__method == 'GET':
#             self.__response = self.__service.get_data(data=self.__query_filters)
#         else:
#             self.__response = self.__service.delete_data(instance_primary_key=self.__data.get('address_id'))
#
#     def process(self):
#         return self.__response
#
#
# class AddressView(APIView):
#
#     def post(self, request):
#         data = request.data
#         return AddressUtil(data=data, serializer_class=AddressSerializer(data=data), method='POST').main()
#
#     def get(self, request):
#         query_options = request.query_params
#         return AddressUtil(data=query_options, method='GET').main()
#
#     def patch(self, request):
#         data = request.data
#         return AddressUtil(data=data, serializer_class=AddressSerializer(data=data), method='PATCH').main()
#
#     def delete(self, request):
#         data = {'address_id': request.GET.get('address_id')}
#         return AddressUtil(data=data, method='DELETE').main()
