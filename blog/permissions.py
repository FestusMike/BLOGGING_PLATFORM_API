from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    #Checks if the authenticated user is the author of the post

    def has_permission(self, request, view):
        return request.user.is_authenticated is True
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user