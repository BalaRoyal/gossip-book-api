from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin


class NestedRouter(NestedRouterMixin, DefaultRouter):
    """
    Create nested router 
    """
    pass
