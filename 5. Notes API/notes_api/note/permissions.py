from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.owner==request.user
    
class IsOwnerOrSharedReadOnly(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.owner == request.user or request.user in obj.shared_with.all()
        return obj.owner == request.user