from django import views
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Sum, Q
from rest_framework import viewsets, mixins, views
from rest_framework.response import Response
from rest_framework import permissions
from django_filters import rest_framework as filters

from api.models import InfectedReport, Survivor, Inventory
from api.serializers import (
    InfectedReportSerializer, InventorySerializer, SurvivorSerializer, 
    TradeSerializer, UpdateSurvivorSerializer,
    CreateSurvivorSerializer
)


class IsNotInfected(permissions.BasePermission):
    """ 
    Allows only uninfected survivors to access items. 
    """
    message = "Survivor cannot access your inventory. She is infected." 

    def has_object_permission(self, request, view, obj):
        return not obj.survivor.is_infected


class SurvivorList(viewsets.ModelViewSet):
    """
    Lists all infected survivors e uninfected, Retrieve or creates um survivor.
    """
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('is_infected',)
    http_method_names = ('get', 'post', 'patch')

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return UpdateSurvivorSerializer
        elif self.action == 'create':
            return CreateSurvivorSerializer
        return self.serializer_class


class InventoryRetrieve(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    Retrieves an inventory on one survivor not infected.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = (IsNotInfected,)
    authentication_classes = ()

    def get_object(self):
        return super().get_object()

class ReportInfectedView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    Informs on one infected survivor.
    """
    queryset = InfectedReport.objects.all()
    serializer_class = InfectedReportSerializer


class TradeView(views.APIView):
    """
    Performs an item trade between two uninfected survivors.
    """
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = TradeSerializer(data=data)
        if serializer.is_valid(True):
            serializer.save()
            return Response(serializer.data)


class InfectedReportsView(views.APIView):
    """
    Reports the total number and percentage of infections.
    """
    queryset = Survivor.objects.all()

    def get(self, request, *args, **kwargs):
        infected = Count('pk', filter=Q(is_infected=True))
        query = self.queryset.aggregate(total=Count('pk'), infected=infected)
        value = query['infected'] / query['total']
        data = {
            'infected': query['infected'],
            'percentage': "{:.2%}".format(value)
        }
        return Response(data)


class UninfectedReportsView(views.APIView):
    """
    Reports the total number and percentage of uninfected.
    """
    queryset = Survivor.objects.all()

    def get(self, request, *args, **kwargs):
        uninfected = Count('pk', filter=Q(is_infected=False))
        query = self.queryset.aggregate(total=Count('pk'), uninfected=uninfected)
        value = query['uninfected'] / query['total']
        data = {
            'uninfected': query['uninfected'],
            'percentage': "{:.2%}".format(value)
        }
        return Response(data)

class AverageResourcesView(views.APIView):
    """
    Reports the average number of resources per uninfected survivor.
    """
    queryset = Inventory.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(survivor__is_infected=False)
        items = Inventory.ItemValue.labels
        params = {item.lower(): Sum(item.lower()) for item in items}

        return queryset.aggregate(total_survivor=Count('pk'), **params)

    def get(self, request, *args, **kwargs):
        query = self.get_queryset(*args, **kwargs)
        total = query.pop('total_survivor')
        data = {}
        for key, value in query.items():
            label = f"avg_{key}"
            data[label] = value / total
        return Response(data)


class LostPointsView(views.APIView):
    """
    Reports the number of points lost per infected survivor.
    """
    queryset = Inventory.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(survivor__is_infected=True)
        items = Inventory.ItemValue.labels
        params = {item.lower(): Sum(item.lower()) for item in items}

        return queryset.aggregate(**params)

    def get(self, request, *args, **kwargs):
        query = self.get_queryset(*args, **kwargs)
        data = {
            'lost_points': sum(query.values())
        }
        return Response(data)