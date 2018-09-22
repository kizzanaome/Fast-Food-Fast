import unittest
from app import create_app
from flask import current_app
import json
from .test_data import food_item
from app.food_items.models import food_items


class FoodItems(unittest.TestCase):
    def setUp(self):
        """
            This method is run at the beginig of each test
            also initialises the client where tests will be run

        """
        config_name = 'development'
        self.app = create_app(config_name)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client

        
    def test_place_a_food_item(self):
        """
            method tests post endpoint status_code
        """
    
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(food_item))

        self.assertEqual(response.status_code, 201)

    def test_adding_existing_food_item(self):
        """Method for posting and alredy existing food_item"""

        """ Test for posting food_item successfully """
        response = self.client().post("/api/v1/food_items",
                                      content_type='application/json',
                                      data=json.dumps(food_item))
        self.assertEqual(response.status_code, 201)
        response = self.client().post("/api/v1/food_items",
                                      content_type='application/json',
                                      data=json.dumps(food_item))
        self.assertEqual(response.status_code, 400)

    def test_fetch_all_food_items(self):
       
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(food_item)
                                      )
        self.assertEqual(response.status_code, 201)

        response2 = self.client().get('/api/v1/food_items')
        self.assertEqual(response2.status_code, 200)

    
    def tearDown(self):
        """
        Method to tidy up lists after the test is run
        """
        food_items[:] = []

