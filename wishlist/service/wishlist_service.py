
from utility.crud_helper import CrudHelper
from wishlist.wishlist_serializers.wishlist_serializer import WishlistSerializer


class WishlistService:

    __wishlist_curd_helper = CrudHelper(WishlistSerializer)

    def creat_wishlist(self, data):
        return self.__wishlist_curd_helper.add_obj(data)

    def get_wishlist(self, data):
        if len(data) == 0:
            return self.__wishlist_curd_helper.get_all_data()
        elif len(data) == 1 and data.get('wishlist_id') is not None:
            return self.__wishlist_curd_helper.get_data_by_id(id=data.get('wishlist_id'))
        else:
            query_options_available = ['user', 'subscriber', 'item_id', 'item_details', 'item_added_at']
            filter_query = {}
            for i in query_options_available:
                opt = data.get(i)
                if opt is not None:
                    filter_query[i] = opt

            return self.__wishlist_curd_helper.get_all_data(query=filter_query)

    def update_wishlist(self, data, instance_primary_key):
        return self.__wishlist_curd_helper.update_obj(data, update_key_value=instance_primary_key)

    def delete_wishlist(self, instance_primary_key):
        return self.__wishlist_curd_helper.delete_obj(instance_primary_key)

