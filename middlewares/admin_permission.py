from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        if request.method == "GET" or request.user.is_superuser:
            return True

        return False



class StrictOnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser