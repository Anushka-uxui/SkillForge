from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Allows access only to Admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'Admin')

class IsInstructor(BasePermission):
    """
    Allows access only to Instructor users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'Instructor')

class IsStudent(BasePermission):
    """
    Allows access only to Student users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'Student')
