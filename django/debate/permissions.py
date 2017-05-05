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


class IsContactOrReadOnly(IsAuthenticatedOrReadOnly):
    """Custom permission to only allow contact of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        """True iif method is safe or if owners are user."""
        result = super(IsContactOrReadOnly, self).has_object_permission(
            request, view, obj
        )

        if not result:
            result = obj.contact.id == request.user.id

        return result


class IsOrganizerOrReadOnly(IsAuthenticatedOrReadOnly):
    """Custom permission to only allow organizers to edit it."""

    def has_object_permission(self, request, view, obj):
        """True iif method is safe or if suppliers are user."""
        result = super(IsOrganizerOrReadOnly, self).has_object_permission(
            request, view, obj
        )

        if not result:
            result = obj.organizers.filter(pk=request.user.id).exist()

        return result
