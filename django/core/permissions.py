"""Permisssion module."""
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)


class IsVoter(IsAuthenticated):
    """Custom permission to only allow voter to read/edit its vote."""

    def has_object_permission(self, request, view, obj):
        """True iif method is safe and if user is the voter."""
        result = super(IsVoter, self).has_object_permission(
            request, view, obj
        )

        if not result:
            result = obj.account.id == request.user.id

        return result


class IsAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """Custom permission to only allow admin of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        """True iif method is safe or if admins are user."""
        result = super(IsAdminOrReadOnly, self).has_object_permission(
            request, view, obj
        )

        if not result:
            result = obj.admin.id == request.user.id

        return result
