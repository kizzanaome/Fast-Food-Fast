from flask import Flask, jsonify, make_response
from flask_restful import Resource, reqparse
from .models import Food, food_items
import re
import string

class FoodItems(Resource):

    def get(self):
        if not food_items:
            return {"massage": "food_items are not created yet"}, 200
        return {"Food_items": food_items}, 200

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("food_name",
                            type=str,
                            required=True,
                            help="The food_name field can't be empty",
                            location='json')
        parser.add_argument("price",
                            type=int,
                            required=True,
                            help="Price cant be coverted ")
        args = parser.parse_args()

        """auto generating food_id"""

        if len(food_items)==0:       
            food_id = len(food_items)+1
        food_id = len(food_items)+1

        """ validate data sent """

        if not args['food_name']:
            return make_response(jsonify({"message":
                                          "Add food_name"}),
                                 401)

        if args['price'] == "":
            return make_response(jsonify({"message":
                                          "Add price"}),
                                 401)

        if re.compile('[!@#$%^&*:;?><.]').match(args['food_name']):
            return {'message': 'Please dont input symbols'}, 400
            
        if re.compile('[   text]').match(args['food_name']):
            return {'message': 'Please avoid adding spaces before characters'}, 400

        if re.compile('[text   0]').match(args['food_name']):
            return {'message': 'Please avoid adding spaces'}, 400


        if len(str(args['food_name'])) < 4:
            return {'message': 'food_name should be more than 4 characters'}, 400

        chars = string.whitespace + string.punctuation + string.digits
        food = Food(food_id, args["food_name"], args["price"])

        for fd in food_items:
            if args['food_name'].strip(chars) == fd['food_name'].strip(chars):
                return make_response(jsonify({"massage": "food_item has alredy been created"}), 400)
        food.create_foodItems()
        return make_response(jsonify({"massage": "food_item has been created succesfully"}), 201)
