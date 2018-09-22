import unittest
from app import create_app
from flask import current_app
import json


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

    def test_app_exixts(self):
        self.assertFalse(current_app is None)

    def test_place_a_food_item(self):
        """
            method tests post endpoint status_code
        """
        mock_data = {
            "food_id": "1",
            "food_name": "meat with all foods",
            "description": "this meal is served with mattoke, rice, lumonde, and muwogo ",
            "price": 20400,
            "status": "out of stock"
        }
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(mock_data))

        self.assertEqual(response.status_code, 201)

    def test_adding_existing_food_item(self):
        """Method for posting and alredy existing food_item"""
        trial_data1 = {
            "food_id": "2",
            "food_name": "superghetti",
            "description": "superghetti plus sallads",
            "price": 10000,
            "status": " Available"
        }
        trial_data1 = {
            "food_id": "2",
            "food_name": "superghetti",
            "description": "superghetti plus sallads",
            "price": 10000,
            "status": " Available"
        }

        """ Test for posting food_item successfully """
        response = self.client().post("/api/v1/food_items",
                                      content_type='application/json',
                                      data=json.dumps(trial_data1))
        self.assertEqual(response.status_code, 201)
        response = self.client().post("/api/v1/food_items",
                                      content_type='application/json',
                                      data=json.dumps(trial_data1))
        self.assertEqual(response.status_code, 400)

    def test_fetch_all_food_items(self):
        trial_data = {
            "food_id": "8",
            "food_name": "mattoke",
            "description": "mattoke mixed stew",
            "price": 20004,
            "status": "out of stock"
        }
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(trial_data)
                                      )
        self.assertEqual(response.status_code, 201)

        response2 = self.client().get('/api/v1/food_items')
        self.assertEqual(response2.status_code, 200)
