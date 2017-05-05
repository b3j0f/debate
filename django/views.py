"""View module."""

from .models import (
    Category, Product, State, Proposal, Location, Supply, Condition, Request,
    Using, Media, Stock, Common, Service
)
from .serializers import (
    CategorySerializer, ProductSerializer, StateSerializer, ProposalSerializer,
    MediaSerializer, UsingSerializer, RequestSerializer, ConditionSerializer,
    SupplySerializer, LocationSerializer, StockSerializer, CommonSerializer,
    ServiceSerializer
)
from .permissions import IsOwnerOrReadOnly, IsSupplierOrReadOnly

from rest_framework.viewsets import ModelViewSet

from copy import deepcopy


class LocationViewSet(ModelViewSet):
    """Location view set."""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_fields = {
        'id': ['exact'],
        'product': ['exact'],
        'longitude': ['exact', 'lte', 'gte'],
        'latitude': ['exact', 'lte', 'gte'],
        'datetime': ['exact', 'lte', 'gte'],
        'address': ['exact']
    }


class SupplyViewSet(ModelViewSet):
    """Supply view set."""

    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    filter_fields = {
        'id': ['exact'],
        'products': ['exact'],
        'dates': ['exact'],
        'name': ['icontains'],
        'description': ['icontains'],
        'amount': ['lge', 'lte', 'exact'],
        'startdate': ['lge', 'lte', 'exact'],
        'duedate': ['lge', 'lte', 'exact'],
        'period': ['icontains']
    }


class ConditionViewSet(ModelViewSet):
    """Condition view set."""

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    filter_fields = {
        'id': ['exact'],
        'name': ['exact', 'icontains'],
        'amount': ['exact', 'gte', 'lte'],
        'description': ['icontains']
    }


class RequestViewSet(ModelViewSet):
    """Request view set."""

    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    filter_fields = {
        'id': ['exact'],
        'products': ['exact'],
        'accounts': ['exact'],
        'vevent': ['exact']
    }


class UsingViewSet(ModelViewSet):
    """Using view set."""

    queryset = Using.objects.all()
    serializer_class = UsingSerializer
    filter_fields = {
        'id': ['exact'],
        'accounts': ['exact'],
        'products': ['exact'],
        'request': ['exact'],
        'startts': ['exact', 'gte', 'lte'],
        'endts': ['exact', 'gte', 'lte']
    }


class MediaViewSet(ModelViewSet):
    """Media view set."""

    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_fields = {
        'id': ['exact'],
        'media': ['exact'],
        'product': ['exact'],
        'state': ['exact']
    }


class ProposalViewSet(ModelViewSet):
    """Proposal view set."""

    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    filter_fields = {
        'id': ['exact'],
        'request': ['exact'],
        'condition': ['exact'],
        'quantity': ['exact', 'gte', 'lte'],
        'description': ['icontains']
    }


class CategoryViewSet(ModelViewSet):
    """Category view set."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_fields = {
        'id': ['exact'],
        'name': ['exact', 'icontains'],
        'types': ['icontains'],
        'parent': ['exact'],
        'description': ['icontains'],
        'children': ['exact']
    }


class CommonViewSet(ModelViewSet):
    """Common view set."""

    queryset = Common.objects.all()
    serializer_class = CommonSerializer
    filter_fields = {
        'id': ['exact'],
        'name': ['exact', 'icontains'],
        'description': ['icontains'],
        'owners': ['exact'],
        'suppliers': ['exact'],
        'users': ['exact'],
        'categories': ['exact', 'icontains'],
        'stock': ['exact'],
        'states': ['exact'],
        'locations': ['exact']
    }
    permission_classes = (IsOwnerOrReadOnly, IsSupplierOrReadOnly)


class ProductViewSet(CommonViewSet):
    """Product view set."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StockViewSet(ProductViewSet):
    """Stock view set."""

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_fields = deepcopy(ProductViewSet.filter_fields)
    filter_fields.update({
        'products': ['exact'],
        'capacities': ['exact'],
        'parent': ['exact']
    })


class ServiceViewSet(CommonViewSet):
    """Service view set."""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_fields = deepcopy(CommonViewSet.filter_fields)
    filter_fields.update({
        'products': ['exact'],
        'capacities': ['exact'],
        'parent': ['exact']
    })


class StateViewSet(ModelViewSet):
    """State view set."""

    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_fields = {
        'name': ['exact'],
        'description': ['icontains']
    }
