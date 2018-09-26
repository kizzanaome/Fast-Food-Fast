import unittest
from app import create_app
from flask import current_app
import json
from app.orders.models import Order,orders_db
from app.food_items.views import food_items
from .test_data import*


class BaseCase(unittest.TestCase):
    """class holds all the unittests for the app"""

    def setUp(self):
        """
            This method is run at the begining of each test
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
        self.order = Order(1,1,"rice and meat","Kampala",3,2000,"pending")
        self.assertIsInstance(self.order, Order)

    def test_app_exixts(self):
        self.assertFalse(current_app is None)

    def test_place_an_order(self):
        """
            method tests post endpoint status_code
        """
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(food_menu))
        self.assertEqual(response.status_code, 201)

        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(post_an_order))

        self.assertEqual(response.status_code, 201)

    def test_adding_order_with_food_id_thats_not_existing(self):
        """method for testing an  inexisting food_item"""
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(food_menu_2))
        self.assertEqual(response.status_code, 201)
        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(post_an_order_with_a_wrong_foodmenu_id))
        self.assertEqual(response.status_code, 404)


    def test_place_order_with_empty_location(self):
        """ Test for empty post validation """
       
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(food_menu))
        self.assertEqual(response.status_code, 201)
        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(post_with_empty_location))
        self.assertEquals(response.status_code, 401)

    def test_place_order_with_quantity_field_not_integer(self):
         """ Test for empty post validation """
      
         response = self.client().post("/api/v1/orders",
                                       content_type='application/json',
                                       data=json.dumps(posting_wrong_datatype_for_quantity_field))
         self.assertEquals(response.status_code, 400)

    def test_place_order_with_short_characters(self):
        """ Test for short post validation """
        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(posting_order_with_short_characters))
        self.assertEquals(response.status_code, 400)

    def test_place_order_with_spaces_before_location(self):
        """ Test for spaces before characters """
        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(posting_order_with_spaces_before_characters))
        self.assertEquals(response.status_code, 400)

    def test_place_order_with_symbols_instead_of_characters(self):
        """ Test for symbols """
        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(posting_order_with_symbols))
        self.assertEquals(response.status_code, 400)


    def test_place_order_with_wrong_url(self):
        """ Test for wrong url input """
        response = self.client().post("/api/v1/orders/",
                                      content_type='application/json',
                                      data=json.dumps(posting_order_with_symbols))
        self.assertEquals(response.status_code, 404)

    def test_fetch_all_orders(self):
        "test for fetching available orders"
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(food_menu))
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(post_an_order)
                                      )
        self.assertEqual(response.status_code, 201)

        response2 = self.client().get('/api/v1/orders')
        self.assertEqual(response2.status_code, 200)

    def test_fetch_orders_which_havenot_been_placed(self):
        """ Test for inexising orders """
        response = self.client().get("/api/v1/orders")
        self.assertEquals(response.status_code, 200)


    def test_update_order_status(self):
        """Method tests wethere the status is updated succesfully"""
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(food_menu))
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(post_an_order)
                                      )
        self.assertEqual(response.status_code, 201)

        response2 = self.client().get('/api/v1/orders/1')
        self.assertEqual(response2.status_code, 200)

        response = self.client().put('api/v1/orders/1',
                                     content_type='application/json', data=json.dumps(updated_status))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Status updated ", str(response.data))

        response2 = self.client().get('/api/v1/orders/1')
        self.assertEqual(response2.status_code, 200)

    def test_fetch_a_single_order(self):
        """tests that get method fetches a single order"""
       
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(food_menu))
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(post_an_order)
                                      )
        self.assertEqual(response.status_code, 201)

        response2 = self.client().get("/api/v1/orders/1")
        self.assertEquals(response2.status_code, 200)

    def test_get_an_id_that_is_not_in_the_list(self):
        '''Test to fetch single order with improper id'''
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(food_menu))
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(post_an_order)
                                      )
        self.assertEqual(response.status_code, 201)

        response2 = self.client().get("/api/v1/orders/2")
        self.assertEqual(response2.status_code, 404)

    def test_delete_an_order(self):
        '''Test to delete a specific'''
        response = self.client().post('/api/v1/food_items',
                                      content_type='application/json', data=json.dumps(food_menu))
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(post_an_order)
                                      )
        self.assertEqual(response.status_code, 201)

        response2 = self.client().get("/api/v1/orders/1")
        self.assertEqual(response2.status_code, 200)

        response = self.client().delete('/api/v1/orders/1')
        self.assertEqual(response.status_code, 200)

        response2 = self.client().get("/api/v1/orders/1")
        self.assertEqual(response2.status_code, 404)

    def tearDown(self):
        """
        Method to tidy up lists after the test is run
        """
        orders_db[:] = []
        food_items[:] = []
