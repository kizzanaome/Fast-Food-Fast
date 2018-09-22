import unittest
from app import create_app
from flask import current_app
import json
from app.orders.models import Order


class BaseCase(unittest.TestCase):
    """class holds all the unittests for the app"""

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

    def test_model_function(self):
        """Tests if the dummy data provided is
            an instance of the order class
        """
        self.order = Order(1, 2, "rice and meat",
                           "one plate", "Kampala", "pending")
        self.assertIsInstance(self.order, Order)

    def test_app_exixts(self):
        self.assertFalse(current_app is None)

    def test_place_an_order(self):
        """

            method tests post endpoint status_code
        """
        post_order = {
            "order_id": "2",
            "food_id": "2",
            "food_name": "rice and greens",
            "quantity": "10 plates",
            "location": "mutundwe",
            "status": "pending"
        }
        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(post_order))

        self.assertEqual(response.status_code, 201)

    def test_adding_existing_order(self):
        """method for testing existing order"""
        trial_data1 = {
            "order_id": "3",
            "food_id": "3",
            "food_name": "luwombo",
            "quantity": "10 plates",
            "location": "mutundwe",
            "status": "pending"
        }
        trial_data1 = {
            "order_id": "3",
            "food_id": "3",
            "food_name": "luwombo",
            "quantity": "10 plates",
            "location": "mutundwe",
            "status": "pending"
        }

        """ Test for posting order successfully """
        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(trial_data1))
        self.assertEqual(response.status_code, 201)
        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(trial_data1))
        self.assertEqual(response.status_code, 400)

    def test_place_order_with_empty_food_name(self):
        """ Test for empty post validation """
        mock_data = {
            "order_id": "5",
            "food_id": "5",
            "food_name": "",
            "quantity": "10 plates",
            "location": "mutundwe",
            "status": "pending"
        }

        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(mock_data))
        self.assertEquals(response.status_code, 401)

    def test_place_order_with_empty_field_quantity(self):
        """ Test for empty post validation """
        mock_data = {
            "order_id": "6",
            "food_id": "6",
            "food_name": "matokekli",
            "quantity": "",
            "location": "mutundwe",
            "status": "pending"
        }

        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(mock_data))
        self.assertEquals(response.status_code, 401)

    def test_place_order_with_short_characters(self):
        """ Test for short post validation """
        mock_data = {
            "order_id": "7",
            "food_id": "7",
            "food_name": "ma",
            "quantity": "10 plates",
            "location": "kitooro",
            "status": "pending"
        }

        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(mock_data))
        self.assertEquals(response.status_code, 400)

    def test_fetch_all_orders(self):
        "test for fetching available orders"
        trial_data = {
            "order_id": "8",
            "food_id": "8",
            "food_name": "rice and fishfillet",
            "quantity": "10 plates",
            "location": "mutundwe",
            "status": "out of stock"
        }
        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(trial_data)
                                      )
        self.assertEqual(response.status_code, 201)

        response2 = self.client().get('/api/v1/orders')
        self.assertEqual(response2.status_code, 200)

    def test_update_order_status(self):
        """Method tests wethere the status is updated succesfully"""
        data_for_updating = {
            "order_id": "9",
            "food_id": "9",
            "food_name": "mallllotoke",
            "quantity": "10 plates",
            "location": "mutundwe",
            "status": "pending"
        }

        response = self.client().post('api/v1/orders',
                                      content_type='application/json', data=json.dumps(data_for_updating))

        self.assertEqual(response.status_code, 201)

        response = self.client().put('api/v1/orders/1',
                                     content_type='application/json', data=json.dumps(data_for_updating))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Status updated ", str(response.data))

    def test_fetch_a_single_order(self):
        """tests that get method fetches a single order"""
        dumm_data = {
            "order_id": "10",
            "food_id": "9",
            "food_name": "posho and beans",
            "quantity": "10 plates",
            "location": "mutundwe",
            "status": "out of stock"
        }
        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(dumm_data))
        self.assertEquals(response.status_code, 201)

        response2 = self.client().get("/api/v1/orders/1",
                                      content_type='application/json', data=json.dumps(dumm_data))
        self.assertEquals(response2.status_code, 200)

    def test_get_an_id_that_is_not_in_the_list(self):
        '''Test to fetch single order with improper id'''
        trial_data1 = {
            "order_id": "10",
            "food_id": "10",
            "food_name": "rice and matooke",
            "quantity": "10 plates",
            "location": "mutundwe",
            "status": "pending"
        }

        trial_data2 = {
            "order_id": 11,
            "food_id": "11",
            "food_name": "lumonde and cassava",
            "quantity": "10 plates",
            "location": "mutundwe",
            "status": "pending"
        }

        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(trial_data1))
        self.assertEqual(response.status_code, 201)
        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(trial_data2))
        self.assertEqual(response.status_code, 201)
        response2 = self.client().get("/api/v1/orders/11")
        self.assertEqual(response2.status_code, 404)

    def test_delete_an_order(self):
        '''Test to delete a specific'''
        trial_data1 = {
            "order_id": 9,
            "food_id": 14,
            "food_name": "rice and superghetti",
            "quantity": "10 plates",
            "location": "mutundwe",
            "status": "pending"
        }
        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(trial_data1))
        self.assertEqual(response.status_code, 201)
        response = self.client().delete('/api/v1/orders/9')
        self.assertEqual(response.status_code, 200)
