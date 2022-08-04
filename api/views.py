from rest_framework import viewsets

from api.models import Survivor, Inventory
from api.serializers import SurvivorSerializer, UpdateSurvivorSerializer


class SurvivorList(viewsets.ModelViewSet):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return UpdateSurvivorSerializer
        return self.serializer_class

