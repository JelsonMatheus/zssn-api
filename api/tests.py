from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import Inventory, Survivor


def create_survivor(name='João', age=12, gender='M', is_infected=False,
                latitude=10, longitude=120, inventory=None):

    if inventory is None:
        items = {'water': 6, 'food': 3, 'medication': 5, 'ammunition': 1}
        inventory = Inventory(**items)

    survivor = Survivor.objects.create(
        name=name, 
        age=age, 
        gender=gender, 
        is_infected=is_infected, 
        latitude=latitude, 
        longitude=longitude,
    )
    inventory.survivor = survivor
    inventory.save()
    
    return survivor    

class InventoryModelTests(APITestCase):
    
    def setUp(self): 
        self.items = {'water': 6, 'food': 3, 'medication': 5, 'ammunition': 1}
        self.unit_items = {'water': 4, 'food': 3, 'medication': 2, 'ammunition': 1}
        self.inventory = Inventory(**self.items)

    def test_total_value_of_each_item(self):
        """
        tests the total points of each item
        """
        for name, value in self.items.items():
            unit = self.unit_items[name]
            item_value = self.inventory.get_full_value_item(name)
            self.assertEqual(item_value, (unit * value))

    def test_resource_point_total(self):
        """
        Tests the total resource points of an inventory
        """
        total = 0
        for name, value in self.items.items():
            total += value * self.unit_items[name]
        self.assertEqual(self.inventory.total_resource_value, total)


class InfectedReportsViewTests(APITestCase):
    
    def setUp(self):        
        create_survivor(is_infected=True)
        create_survivor(is_infected=True)
        create_survivor(is_infected=True)
        create_survivor(is_infected=False)
    
    def test_total_infected(self):
        response = self.client.get(reverse('report-infected'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['infected'], 3)
        self.assertEqual(response.data['percentage'], 75.0)


class UninfectedReportsViewTests(APITestCase):
    
    def setUp(self): 
               
        create_survivor(is_infected=True)
        create_survivor(is_infected=True)
        create_survivor(is_infected=True)
        create_survivor(is_infected=False)
    
    def test_total_unifected(self):
        response = self.client.get(reverse('report-uninfected'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uninfected'], 1)
        self.assertEqual(response.data['percentage'], 25)


class AverageResourcesViewTests(APITestCase):

    def setUp(self):
        inventory1 = Inventory(water=1)
        inventory2 = Inventory(water=3, food=2)
        inventory3 = Inventory(medication=1, ammunition=1)
        inventory4 = Inventory()

        create_survivor(inventory=inventory1)
        create_survivor(inventory=inventory2)
        create_survivor(inventory=inventory3)
        create_survivor(inventory=inventory4)

    
    def test_average_resource(self):
        response = self.client.get(reverse('avg-resources'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['avg_water'], 1)
        self.assertEqual(response.data['avg_food'], 0.5)
        self.assertEqual(response.data['avg_medication'], 0.25)
        self.assertEqual(response.data['avg_ammunition'], 0.25)
    

class LostPointsViewTests(APITestCase):

    def setUp(self):
        inventory1 = Inventory(water=2)
        inventory2 = Inventory(food=1)

        create_survivor(is_infected=True, inventory=inventory1)
        create_survivor(is_infected=True, inventory=inventory2)
    
    def test_average_resource(self):
        response = self.client.get(reverse('lost-points'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lost_points'], 11)