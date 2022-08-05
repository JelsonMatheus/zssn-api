from rest_framework import viewsets, mixins

from api.models import InfectedReport, Survivor, Inventory
from api.serializers import (
    InfectedReportSerializer, SurvivorSerializer, UpdateSurvivorSerializer
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

        


