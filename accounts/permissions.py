from rest_framework.permissions import BasePermission

from accounts.models import User


class IsRole(BasePermission):
    required_roles = ()

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role in self.required_roles or user.is_superuser


class IsTeachingStaff(IsRole):
    required_roles = (User.TEACHING_STAFF, User.ADMINISTRATOR)


class IsNonTeachingStaff(IsRole):
    required_roles = (User.NON_TEACHING_STAFF, User.ADMINISTRATOR)


class IsParent(IsRole):
    required_roles = (User.PARENT, User.ADMINISTRATOR)


class IsStudent(IsRole):
    required_roles = (User.STUDENT, User.ADMINISTRATOR)
