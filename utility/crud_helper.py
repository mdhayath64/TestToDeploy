import traceback
from abc import abstractmethod
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from utility.common_utils import serializer_instance, custom_response_obj

"""
    Author:-Saif Ali Khan
    One master class to handle crud operations with additional business logics, 

    methods to add and scope of improvements
        1.Bulk insert or update
        2.get or create
        3.advanced queries
        4.If a model has one or multiple foreign keys objects that has to be created

    work around for above can be achieved by overriding the below methods
"""


class CrudHelper:

    def __init__(self, serializer):
        self.__serializer = serializer
        self.__model_class = serializer.Meta.model

    @abstractmethod
    def add_obj(self, data, validate_add=False, validate_model=None, value=None, **kwargs):

        if validate_add:
            validate_app = self.__validate(data=data, validate_model=validate_model, value=value)
            if validate_app:
                pass
            else:
                return custom_response_obj(data=None,message='Given data does not exist', code=404)
        return serializer_instance(self.__serializer, data=data, **kwargs)

    @abstractmethod
    def update_obj(self, data, update_key_value=None):
        validate_app = self.__validate(data=data, value=update_key_value)
        if validate_app:
            return serializer_instance(self.__serializer, instance=validate_app, data=data, partial=True)
        else:
            return custom_response_obj(message='Given data does not exist', code=404,data=None)

    @abstractmethod
    def get_all_data(self, query=None, annotate=None, values_list=None, request=None, pre_fetch=None, paginate=None,exclude=None, order_by_option='-created_at'):

        custom_resp = False
        response=None
        if query is None and exclude is None:
            objs = self.__model_class.objects.all().order_by(order_by_option)
        elif exclude is not None:
            objs = self.__model_class.objects.exclude(**exclude).all().order_by(order_by_option)
        else:
            objs = self.__model_class.objects.filter(**query).order_by(order_by_option)


        if pre_fetch is not None:
            custom_resp = True
            objs=objs.prefetch_related(*pre_fetch)
        if values_list is not None:
            custom_resp = True
            objs = objs.values(*values_list)
        if annotate is not None:
            objs = objs.annotate(**annotate)
            custom_resp=True

        if paginate is not None:
            custom_resp=True
            paginate=paginate()
            paginated_data=paginate.paginate_queryset(objs, request)
            serializer_data=self.__serializer(paginated_data, many=True).data
            response=paginate.get_paginated_response(serializer_data).data
            objs=response.pop('results')

        if custom_resp:
            count = response.pop('count')
            next=response.pop('next')
            prev=response.pop('previous')

            resp = custom_response_obj(message='request processed successfully', code=200,data=objs, count=count, next=next, prev=prev)
        else:
            resp=serializer_instance(serializer_instance=self.__serializer,
                                   read_only=True, data=objs,
                                many=True)

        return resp

    @abstractmethod
    def get_latest_data(self, latest_key):
        try:
            obj = self.__model_class.objects.latest(latest_key)
            return serializer_instance(serializer_instance=self.__serializer,
                                       read_only=True, data=obj,
                                       many=False)
        except Exception as e:
            traceback.print_exc()
            return custom_response_obj(message=str(e), code=500,data=None)

    @abstractmethod
    def get_data_by_id(self, id):
        try:
            pk_name = self.__model_class._meta.pk.name
            query = Q(**{pk_name: id})
            obj = self.__model_class.objects.get(query)
            return serializer_instance(serializer_instance=self.__serializer,
                                       read_only=True, data=obj,
                                       many=False)
        except ObjectDoesNotExist:
            return custom_response_obj(message='Data does not exist', code=404,data=None)

        except Exception as e:
            print('exception')
            return custom_response_obj(message=f'Internal server error {e}', code=500,data=None)

    def __validate(self, data, validate_model=None, value=None):
        try:
            model_to_use = self.__model_class if validate_model is None else validate_model
            pk_name = model_to_use._meta.pk.name
            value = value if value is not None else data.get(pk_name, None)
            query = Q(**{pk_name: value})
            obj = model_to_use.objects.get(query)
            """
                to access primary key use obj._meta.pk
            """
            return obj
        except ObjectDoesNotExist:
            return None
        except Exception:
            return None

    @abstractmethod
    def delete_obj(self, id):
        try:
            pk_name = self.__model_class._meta.pk.name
            query = Q(**{pk_name: id})
            self.__model_class.objects.get(query).delete()
            return custom_response_obj(message={'msg': 'Data deleted successfully'}, code=200,data=None)
        except ObjectDoesNotExist:
            return custom_response_obj(message={'msg': 'Data does not exist'}, code=404, data=None)
        except Exception as e:
            return custom_response_obj(message={'msg': f'Internal server error {e}'}, code=500, data=None)

    @abstractmethod
    def delete_multiple_obj(self, id_list):
        try:
            pk_name = self.__model_class._meta.pk.name
            query = Q(**{pk_name+'__in': id_list})
            print(query)
            self.__model_class.objects.filter(query).delete()
            return custom_response_obj(message={'msg': 'Data deleted successfully'}, code=200, data=None)
        except ObjectDoesNotExist:
            return custom_response_obj(message={'msg': 'Data does not exist'}, code=404, data=None)
        except Exception as e:
            return custom_response_obj(message={'msg': f'Internal server error {e}'}, code=500, data=None)



