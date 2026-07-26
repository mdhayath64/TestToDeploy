#
# from utility.crud_helper import CrudHelper
#
#
# class AddressService:
#     __user_crud_helper = CrudHelper(AddressSerializer)
#
#     """
#         creates an obj in Address table
#     """
#
#     def add_address(self, data):
#         return self.__user_crud_helper.add_obj(data)
#
#     """
#         get data by id , Id will always be primary key
#         if id is not provided then return all data
#     """
#
#     def get_data(self, data):
#         if len(data) == 0:
#             return self.__user_crud_helper.get_all_data()
#         elif len(data) == 1 and data.get('address_id') is not None:
#             return self.__user_crud_helper.get_data_by_id(id=data.get('address_id'))
#         else:
#             query_options_available = ['city', 'state', 'pincode', 'country', 'user']
#             filter_query = {}
#             for i in query_options_available:
#                 opt = data.get(i)
#                 if opt is not None:
#                     filter_query[i] = opt
#
#             return self.__user_crud_helper.get_all_data(query=filter_query)
#
#     """
#         updates table obj using update data and primary key of the obj
#         that is currently being updated
#     """
#
#     def update_data(self, data, instance_primary_key):
#         return self.__user_crud_helper.update_obj(data, update_key_value=instance_primary_key)
#
#     """
#         Deletes data against the primary key
#     """
#
#     def delete_data(self, instance_primary_key):
#         return self.__user_crud_helper.delete_obj(instance_primary_key)
