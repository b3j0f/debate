"""Serialization module."""

from .models import (
    Account, Topic, Media, Event, Space, Tag, Vote, Stat
)
from .permissions import IsVoter, IsAdminOrReadOnly

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


class TopicSerializer(HyperlinkedModelSerializer):
    """Topic serializer."""

    permission_classes = (IsAdminOrReadOnly,)

    class Meta:
        """Group serializer meta class."""

        model = Topic
        fields = [
            'contact', 'name', 'description', 'public', 'score', 'medias'
        ]


class MediaSerializer(HyperlinkedModelSerializer):
    """Media serializer."""

    class Meta:
        """Media serializer meta class."""

        model = Media
        fields = ['file', 'url', 'topic']


class EventSerializer(HyperlinkedModelSerializer):
    """Event serializer."""

    class Meta:
        """Event serializer meta class."""

        model = Event
        fields = ['date', 'mduration', 'space', 'topics', 'spaces']


class SpaceSerializer(HyperlinkedModelSerializer):
    """Space serializer."""

    permission_classes = (IsAdminOrReadOnly, )

    class Meta:
        """Space serializer meta class."""

        model = Space
        fields = [
            'admins', 'address', 'lon', 'lat', 'sortedtopics', 'medias',
            'name', 'description'
        ]


class VoteSerializer(HyperlinkedModelSerializer):
    """Vote serializer."""

    permission_classes = (IsVoter, )

    class Meta:
        """Vote serializer meta class."""

        model = Vote
        fields = ['account', 'topic', 'value']


class TagSerializer(HyperlinkedModelSerializer):
    """Tag serializer."""

    class Meta:
        """Tag serializer meta class."""

        model = Tag
        fields = ['name', 'tagged']


class StatSerializer(HyperlinkedModelSerializer):
    """Stat serializer."""

    class Meta:
        """Stat serializer meta class."""

        model = Stat
        fields = ['date', 'accounts', 'Topics', 'Spaces', 'votes']
