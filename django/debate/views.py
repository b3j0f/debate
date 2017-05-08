"""View module."""

from .models import (
    Account, User, Debate, Scheduling, Organization, Vote, Category, Media,
    Stat
)
from .serializers import (
    AccountSerializer, UserSerializer, DebateSerializer, MediaSerializer,
    SchedulingSerializer, VoteSerializer, CategorySerializer,
    OrganizationSerializer, StatSerializer
)
from .permissions import IsVoter, IsContactOrReadOnly, IsOrganizerOrReadOnly

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


class DebateViewSet(ModelViewSet):
    """Debate view set."""

    queryset = Debate.objects.all()
    serializer_class = DebateSerializer
    filter_fields = {
        'id': ['exact'],
        'contact': ['exact'],
        'name': ['exact', 'icontains'],
        'public': ['exact'],
        'score': ['lte', 'gte', 'exact'],
        'description': ['icontains'],
        'medias': ['exact']
    }
    permission_classes = (IsContactOrReadOnly,)


class MediaViewSet(ModelViewSet):
    """Media view set."""

    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_fields = {
        'id': ['exact'],
        'file': ['exact'],
        'url': ['icontains'],
        'debate': ['exact']
    }


class SchedulingViewSet(ModelViewSet):
    """Scheduling view set."""

    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer
    filter_fields = {
        'id': ['exact'],
        'date': ['exact', 'lte', 'gte'],
        'mduration': ['exact', 'lte', 'gte'],
        'organization': ['exact']
    }


class OrganizationViewSet(ModelViewSet):
    """Organization view set."""

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_fields = {
        'id': ['exact'],
        'Organization': ['exact'],
        'product': ['exact'],
        'state': ['exact']
    }
    permission_classes = (IsOrganizerOrReadOnly,)


class VoteViewSet(ModelViewSet):
    """Vote view set."""

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_fields = {
        'id': ['exact'],
        'account': ['exact'],
        'debate': ['exact'],
        'value': ['exact', 'gte', 'lte']
    }
    permission_classes = (IsVoter,)


class CategoryViewSet(ModelViewSet):
    """Category view set."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_fields = {
        'id': ['exact'],
        'name': ['exact', 'icontains'],
        'description': ['icontains'],
        'debates': ['exact']
    }


class StatViewSet(ModelViewSet):
    """Stat view set."""

    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    filter_fields = {
        'id': ['exact'],
        'date': ['exact', 'lte', 'gte'],
        'accounts': ['exact', 'lte', 'gte'],
        'organizations': ['exact', 'lte', 'gte'],
        'votes': ['exact', 'lte', 'gte'],
    }
