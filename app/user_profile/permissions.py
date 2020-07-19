from rest_framework import permissions


class IsProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Allows only profile owners to update their accounts.
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class IsFollowerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Allows only profile owners to update their accounts.
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id
