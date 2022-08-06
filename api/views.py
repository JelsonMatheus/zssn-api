from django import views
from django.utils.translation import gettext_lazy as _
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
            