from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return Subscription.objects.filter(user=request.user, course_id=view.kwargs.get('course_id')).exists()

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
      
    

class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS


def is_admin(func):
    @wraps(func)    
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail: sorry, is staff_only'})
        return func(self, request, *args, **kwargs)
    return wrapper
