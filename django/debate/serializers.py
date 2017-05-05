"""Serialization module."""

from .models import (
    Account, Debate, Media, Scheduling, Organization, Category, Vote, Stat
)
from .permissions import IsVoter, IsContactOrReadOnly, IsOrganizerOrReadOnly

from django.contrib.auth.models import User

from rest_framework.serializers import HyperlinkedModelSerializer


class AccountSerializer(HyperlinkedModelSerializer):
    """Account serializer."""

    class Meta:
        """Account serializer meta class."""

        model = Account
        fields = ['user', 'avatar', 'relationships', 'address, languages']


class UserSerializer(HyperlinkedModelSerializer):
    """User serializer."""

    class Meta:
        """User serializer meta class."""

        model = User
        fields = ['account']


class DebateSerializer(HyperlinkedModelSerializer):
    """Debate serializer."""

    permission_classes = (IsContactOrReadOnly,)

    class Meta:
        """Group serializer meta class."""

        model = Debate
        fields = [
            'contact', 'name', 'description', 'public', 'state', 'score',
            'medias', 'mduration'
        ]


class MediaSerializer(HyperlinkedModelSerializer):
    """Media serializer."""

    class Meta:
        """Media serializer meta class."""

        model = Media
        fields = ['file', 'url', 'debate']


class SchedulingSerializer(HyperlinkedModelSerializer):
    """Scheduling serializer."""

    class Meta:
        """Scheduling serializer meta class."""

        model = Scheduling
        fields = ['date', 'mduration', 'organization']


class OrganizationSerializer(HyperlinkedModelSerializer):
    """Organization serializer."""

    permission_classes = (IsOrganizerOrReadOnly, )

    class Meta:
        """Organization serializer meta class."""

        model = Organization
        fields = [
            'organizers', 'address', 'lon', 'lat', 'sorteddebates', 'medias',
            'name', 'description'
        ]


class VoteSerializer(HyperlinkedModelSerializer):
    """Vote serializer."""

    permission_classes = (IsVoter, )

    class Meta:
        """Vote serializer meta class."""

        model = Vote
        fields = ['account', 'debate', 'value']


class CategorySerializer(HyperlinkedModelSerializer):
    """Category serializer."""

    class Meta:
        """Category serializer meta class."""

        model = Category
        fields = ['name', 'description', 'debates']


class StatSerializer(HyperlinkedModelSerializer):
    """Stat serializer."""

    class Meta:
        """Stat serializer meta class."""

        model = Stat
        fields = ['date', 'accounts', 'debates', 'organizations', 'votes']
