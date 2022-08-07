from django import views
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Sum, Q
from rest_framework import viewsets, mixins, views
from rest_framework.response import Response

from api.models import InfectedReport, Survivor, Inventory
from api.serializers import (
    InfectedReportSerializer, SurvivorSerializer, TradeSerializer, UpdateSurvivorSerializer
)


class SurvivorList(viewsets.ModelViewSet):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    http_method_names = ('get', 'post', 'patch')

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return UpdateSurvivorSerializer
        return self.serializer_class


class ReportInfectedView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = InfectedReport.objects.all()
    serializer_class = InfectedReportSerializer


class TradeView(views.APIView):
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = TradeSerializer(data=data)
        if serializer.is_valid(True):
            serializer.save()
            return Response(serializer.data)


class InfectedReportsView(views.APIView):
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