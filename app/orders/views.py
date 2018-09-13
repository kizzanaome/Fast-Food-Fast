from flask import Flask, make_response, jsonify
from flask_restful import reqparse, Resource
from .models import Order, orders_db
from .validate import clean_input
from app.food_items.models import Food, food_items


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
        parser = reqparse.RequestParser()
        parser.add_argument("food_name",
                            type=str,
                            required=True,
                            help="The food_category field can't be empty")
        parser.add_argument("quantity",
                            type=str,
                            required=True,
                            help="The quantity field cant be empty")
        parser.add_argument("location",
                            type=str,
                            required=True,
                            help="The location field cant be empty")

        args = parser.parse_args()

        """ validate data sent """

        if not args['food_name']:
            return make_response(jsonify({"message":
                                          "Please add the name of the food"}),
                                 401)
        if not args['quantity']:
            return make_response(jsonify({"message":
                                          "Add quantity"}),
                                 401)

        if not args['location']:
            return make_response(jsonify({"message":
                                          "Please add your location"}),
                                 401)

        if len(str(args['food_name'])) < 4:
            return {'message': 'This field should be more than four characters'}, 400

        """
        auto generating the order_id 
            
        """
        if len(orders_db) == 0:
            order_id = len(orders_db)+1
        else:
            order_id = len(orders_db)+1

        status = 'pending'

        if len(food_items) == 0:
            food_id = len(food_items)+1
        else:
            food_id = len(food_items)+1
        
        order = Order(order_id, food_id,
                      args["food_name"], args["quantity"], args["location"], status)
        
        for odr in orders_db:
            if args['food_name'].strip(" ") == odr['food_name'].strip(" "):
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
