from flask import Flask, make_response, jsonify
from .models import Order, orders_db
from app.food_items.models import Food, food_items
from flask_restplus import reqparse, Resource
import string
import re

class OrdersList(Resource):

    def get(self):
        """
             This method returns all orders created
        """
        if not orders_db:
            return make_response(jsonify({"message": "No orders placed yet"}), 200)
        return make_response(jsonify({"orders": orders_db}), 200)

    def post(self):
        """ This method adds an order """
        parser = reqparse.RequestParser( )
        parser.add_argument("food_name",
                            type=str,
                            required=True,
                            help="The food_name must cant be empty")
        parser.add_argument("location",
                            type=str,
                            required=True,
                            help="The location feild cant be empty")
        parser.add_argument("quantity",
                            type=int,
                            required=True,
                            help="The quantity field must me an integer")
        args = parser.parse_args()

        """ validate data sent """
        if not args['location']:
            return make_response(jsonify({"message":
                                          "Please add your location"}),
                                 401)

        if not args['food_name']:
            return make_response(jsonify({"message":
                                          "Please add your food_namme"}),
                                 401)


        if not args['quantity']:
            return make_response(jsonify({"message":
                                          "Add quantity"}),
                                 401)
        if re.compile('[!@#$%^&*:;?><.]').match(args['location']):
            return {'message': 'Please dont input symbols'}, 400
            
        if re.compile('[   text]').match(args['location']):
            return {'message': 'Please avoid adding spaces before characters'}, 400

        if re.compile('[text   ]').match(args['location']):
            return {'message': 'Please avoid adding spaces'}, 400

        if len(str(args['location'])) < 4:
            return {'message': 'Location is too short.'}, 400


        """checking if the food menu has been creadted and
           food_id exists on the food menu
        """


        food_name = args['food_name']
        if len(food_items) > 0:
            for item in range(len(food_items)):
                if ((food_items[item]['food_name']) == food_name):
                    _food_name = food_items[item]['food_name']
                    # food_id = food_items[item]['food_id']
                    print(food_name)
                else:
                    return {"message": 
                            "The food item selected doesnt exist on the menu;please select other food_items available on the menu"}, 404
        else:
            return make_response(jsonify({'message': 'foodmenu doesnot exist'}), 404)

           
        """
        auto generating the order_id 
            
        """
        if len(orders_db) == 0:
            order_id = len(orders_db)+1
        else:
            order_id = len(orders_db)+1

        status = 'pending'
        chars = string.whitespace + string.punctuation + string.digits

        """creating an instance of an order class"""
        order = Order(order_id,
                      _food_name, args['location'].strip(chars), args["quantity"], status)

        for oder in orders_db:
            if food_name == oder["food_name"]:
                return make_response(jsonify({"massage": "order has alredy been placed"}), 400)
     
        order.place_an_order()
        return make_response(jsonify({"massage": "Order has been created succesfully"}), 201)


class SingleOrder(Resource):
    def get(self, order_id):
        """
            This method returns a particular order 
            of the id given to it from the list of available orders
        """
        order_item = None
        for order in orders_db:
            if (order['order_id'] == order_id):
                order_item = order
                return make_response(jsonify({"Order": order_item}), 200)
        return make_response(jsonify({"masage": "Item not found"}), 404)

    def put(self, order_id):
        """
             This method updates the status of an order.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("status")
        args = parser.parse_args()
        for order in orders_db:
            if order['order_id'] == order_id:
                order['status'] = args['status']
                return make_response(jsonify({"massage": "Status updated succesfully"}), 200)
        return make_response(jsonify({"massage": "Item not found"}), 404)

    def delete(self, order_id):
        """
             This method deletes an order which has a provided id
        """
        for count, order in enumerate(orders_db):
            if order.get("order_id") == order_id:
                orders_db.pop(count)
                return make_response(jsonify({"massage": "order has been deleted succesfully"}), 200)
        return make_response(jsonify({"massage": "Failled to delete the order"}), 200)
