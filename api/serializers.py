from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from api.models import InfectedReport, Survivor, Inventory

 
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('water', 'food', 'medication', 'ammunition')


class SurvivorSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer()

    class Meta:
        model = Survivor
        fields = ('pk', 'name', 'age', 'sex', 'is_infected', 'latitude', 'longitude', 'inventory')
        read_only_fields = ('is_infected',)
    
    def create(self, validated_data):
        inventory_data = validated_data.pop('inventory')
        survivor = Survivor.objects.create(**validated_data)
        inventory = Inventory.objects.create(survivor=survivor, **inventory_data)

        return survivor

class UpdateSurvivorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = ('pk', 'name', 'is_infected', 'latitude', 'longitude')
        read_only_fields = ('name', 'is_infected')

class InfectedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfectedReport
        fields = ('pk', 'informant', 'infected', 'date_report')
        read_only_fields = ('date_report',)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('informant', 'infected'),
                message=_("The informant has already reported the survivor."),
            ),
        ]
    
    def validate_infected(self, instance):
        data = self.context['request'].data
        if data['infected'] == data['informant']:
            raise serializers.ValidationError(_("The informant cannot be the same as the infected."))
        return instance

    def create(self, validated_data):
        infected_report = InfectedReport.objects.create(**validated_data)
        survivor = validated_data['infected']

        if not survivor.is_infected and survivor.reported.count() > 2:
            survivor.is_infected = True
            survivor.save()

        return infected_report        
        
    

