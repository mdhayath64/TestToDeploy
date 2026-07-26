import enum
import traceback
from rest_framework import permissions


class MapRequestPermissions(enum.Enum):
    POST = 'add'
    GET = 'view'
    DELETE = 'delete'
    PATCH = 'change'
    PUT = 'change'


class AccountPermission(permissions.BasePermission):

    def __init__(self,app_name=None, model_name=None, group_name=None):
        self.__model_name=model_name
        self.__app_name=app_name
        self.__group_name=group_name

    def __call__(self):
        return self

    def has_permission(self, request, view):
        #provide all permissions to the super admin
        try:
            if request.user.is_authenticated and int(request.user.role)==0 or request.method=='GET':
                return True
            else:
                if self.__group_name is None:
                    get_permission_type=getattr(MapRequestPermissions,request.method).value
                    permission_name=self.__app_name+'.'+get_permission_type+'_'+self.__model_name
                    return self.check_permission(request.user, perm=permission_name)
                else:
                    return self.check_group_perm(user=request.user, group_name=self.__group_name)
        except Exception:
            traceback.print_exc()
            return False

    def check_permission(self,user, perm):
        return user.has_perm(perm)

    def check_group_perm(self,user, group_name):
        return user.groups.filter(name=group_name).exists()
