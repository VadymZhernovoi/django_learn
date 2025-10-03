from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_staff


class CanTaskOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_task_owner')

class CanSubtaskOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_subtask_owner')


