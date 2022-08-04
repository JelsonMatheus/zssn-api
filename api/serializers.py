from dataclasses import fields
from rest_framework import serializers
from api.models import Survivor, Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('water', 'food', 'medication', 'ammunition')


class SurvivorSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer()

    class Meta:
        model = Survivor
        fields = ('pk', 'name', 'age', 'sex', 'latitude', 'longitude', 'inventory')
    
    def create(self, validated_data):
        inventory_data = validated_data.pop('inventory')
        survivor = Survivor.objects.create(**validated_data)
        inventory = Inventory.objects.create(survivor=survivor, **inventory_data)

        return survivor

class UpdateSurvivorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = ('pk', 'name', 'latitude', 'longitude')
        read_only_fields = ('pk', 'name')

    

    

