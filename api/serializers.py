from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.models import InfectedReport, Survivor, Inventory

 
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('water', 'food', 'medication', 'ammunition')


class CreateSurvivorSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer()

    class Meta:
        model = Survivor
        fields = ('pk', 'name', 'age', 'gender', 'is_infected', 'latitude', 'longitude', 'inventory')
        read_only_fields = ('is_infected',)
    
    def create(self, validated_data):
        inventory_data = validated_data.pop('inventory')
        survivor = Survivor.objects.create(**validated_data)
        inventory = Inventory.objects.create(survivor=survivor, **inventory_data)
        return survivor


class SurvivorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = ('name', 'age', 'gender', 'is_infected', 'latitude', 'longitude')


class UpdateSurvivorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = ('latitude', 'longitude')


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


class TradeSerializer(serializers.Serializer):
    survivor_seller = serializers.PrimaryKeyRelatedField(queryset=Survivor.objects)
    survivor_buyer = serializers.PrimaryKeyRelatedField(queryset=Survivor.objects)
    sends = InventorySerializer()
    pickup = InventorySerializer()

    def validate_survivor_seller(self, instance):
        return self._validate_infected(instance)

    def validate_survivor_buyer(self, instance):
        return self._validate_infected(instance)
    
    def validate_sends(self, instance):
        return instance

    def validate(self, attrs):
        survivor_seller = attrs.get('survivor_seller')
        survivor_buyer = attrs.get('survivor_buyer')
        sends = attrs.get('sends')
        pickup = attrs.get('pickup')

        if survivor_seller.pk == survivor_buyer.pk:
            msg = _("The 'survivor_seller' cannot be the same as the 'survivor_buyer'.")
            raise serializers.ValidationError(msg)

        self._validate_survivor_items(survivor_seller, sends, 'survivor_seller')
        self._validate_survivor_items(survivor_buyer, pickup, 'survivor_buyer')
        self._validate_trade_poins(sends, pickup)

        return attrs
    
    def create(self, validated_data):
        seller = validated_data.get('survivor_seller').inventory
        buyer = validated_data.get('survivor_buyer').inventory
        sends = validated_data.get('sends')
        pickup = validated_data.get('pickup')
        
        # Swap items between inventories
        self._trade_items(seller, buyer, sends)
        self._trade_items(buyer, seller, pickup)
        seller.save()
        buyer.save()

        return validated_data

    def _validate_infected(self, instance):
        if instance.is_infected:
            raise serializers.ValidationError(_("Trade not allowed. Survivor is infected."))
        return instance
    
    def _validate_survivor_items(self, survivor, resources, field_name):
        errors = {}
        inventory = survivor.inventory
        for item, value in resources.items():
            survivor_item = getattr(inventory, item)
            if survivor_item < value:
                msg = _(f"Survivor only has an amount {survivor_item} not {value}.")
                errors[item] = msg
        if errors:
            raise serializers.ValidationError({field_name: errors})
    
    def _validate_trade_poins(self, sends, pickup):
        from_inventory = Inventory(**sends)
        to_inventory = Inventory(**pickup)

        if (from_inventory.total_resource_value 
                != to_inventory.total_resource_value):
            msg = _("The amount of points in the exchange is non-equivalent.")
            raise serializers.ValidationError(msg)
    
    def _trade_items(self, from_inventory, to_inventory, items):
        for name, value in items.items():
            rest = getattr(from_inventory, name) - value
            total = getattr(to_inventory, name) + value
            setattr(from_inventory, name, rest)
            setattr(to_inventory, name, total)
