from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):
    """
    Allow users to Modify question/Gossip only if they own it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        try:
            return obj.user.id == request.user.id
        except Exception:
            return obj.voted_by.id == request.user.id
