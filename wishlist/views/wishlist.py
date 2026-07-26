
from rest_framework.views import APIView
from utility.api_framework import ApiFramework
from wishlist.service.wishlist_service import WishlistService
from wishlist.wishlist_serializers.wishlist_serializer import WishlistSerializer


class OrderUtil(ApiFramework):

    def __init__(self, data, serializer_class=None, **kwargs):
        super().__init__(serializer_class=serializer_class)
        self.__data = data
        self.__response = {}
        self.__service = WishlistService()
        self.__method = kwargs.get('method')
        self.__query_filters = {}

    def format_request(self):
        if self.__method == 'GET':
            for key, value in self.__data.items():
                self.__query_filters[key] = self.__data.get(key)

    def run_logic(self):
        if self.__method == 'POST':
            self.__response = self.__service.creat_wishlist(data=self.__data)
        elif self.__method == 'PATCH':
            self.__response = self.__service.update_wishlist(data=self.__data, instance_primary_key=self.__data
                                                             .get('wishlist_id'))
        elif self.__method == 'GET':
            self.__response = self.__service.get_wishlist(data=self.__query_filters)
        else:
            self.__response = self.__service.delete_wishlist(instance_primary_key=self.__data.get('wishlist_id'))

    def process(self):
        return self.__response


class WishlistView(APIView):
    def post(self, request):
        data = request.data
        return OrderUtil(data=data, serializer_class=WishlistSerializer(data=data), method='POST').main()

    def get(self, request):
        query_options = request.query_params
        return OrderUtil(data=query_options,  method='GET').main()

    def patch(self, request):
        data = request.data
        return OrderUtil(data=data, serializer_class=WishlistSerializer(data=data), method='PATCH').main()

    def delete(self, request):
        data = {'wishlist_id': request.GET.get('wishlist_id')}
        return OrderUtil(data=data, method='DELETE').main()

