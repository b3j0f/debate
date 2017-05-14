"""View module."""

from .models import (
    Account, User, Topic, Scheduling, Space, Vote, Tag, Media,
    Stat
)
from .serializers import (
    AccountSerializer, UserSerializer, TopicSerializer, MediaSerializer,
    SchedulingSerializer, VoteSerializer, TagSerializer,
    SpaceSerializer, StatSerializer
)
from .permissions import IsVoter, IsAdminOrReadOnly

from rest_framework.viewsets import ModelViewSet


class AccountViewSet(ModelViewSet):
    """Account view set."""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_fields = {
        'id': ['exact'],
        'user': ['exact'],
        'avatar': ['exact'],
        'relationships': ['exact'],
        'address': ['iexact'],
        'languages': ['iexact']
    }


class UserViewSet(ModelViewSet):
    """User view set."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = {
        'id': ['exact'],
        'account': ['exact'],
    }


class TopicViewSet(ModelViewSet):
    """Topic view set."""

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_fields = {
        'id': ['exact'],
        'contact': ['exact'],
        'name': ['exact', 'icontains'],
        'public': ['exact'],
        'score': ['lte', 'gte', 'exact'],
        'description': ['icontains'],
        'medias': ['exact']
    }
    permission_classes = (IsAdminOrReadOnly,)


class MediaViewSet(ModelViewSet):
    """Media view set."""

    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_fields = {
        'id': ['exact'],
        'file': ['exact'],
        'url': ['icontains'],
        'topic': ['exact']
    }


class SchedulingViewSet(ModelViewSet):
    """Scheduling view set."""

    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer
    filter_fields = {
        'id': ['exact'],
        'date': ['exact', 'lte', 'gte'],
        'mduration': ['exact', 'lte', 'gte'],
        'Space': ['exact']
    }


class SpaceViewSet(ModelViewSet):
    """Space view set."""

    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    filter_fields = {
        'id': ['exact'],
        'space': ['exact'],
        'product': ['exact'],
        'state': ['exact']
    }
    permission_classes = (IsAdminOrReadOnly,)


class VoteViewSet(ModelViewSet):
    """Vote view set."""

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_fields = {
        'id': ['exact'],
        'account': ['exact'],
        'topic': ['exact'],
        'value': ['exact', 'gte', 'lte']
    }
    permission_classes = (IsVoter,)


class TagViewSet(ModelViewSet):
    """Tag view set."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_fields = {
        'id': ['exact'],
        'name': ['exact', 'icontains'],
        'description': ['icontains'],
        'topicS': ['exact']
    }


class StatViewSet(ModelViewSet):
    """Stat view set."""

    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    filter_fields = {
        'id': ['exact'],
        'date': ['exact', 'lte', 'gte'],
        'accounts': ['exact', 'lte', 'gte'],
        'spaces': ['exact', 'lte', 'gte'],
        'votes': ['exact', 'lte', 'gte'],
    }
