from flask import Flask, jsonify, make_response
from flask_restful import Resource, reqparse
from .models import Food, food_items


class FoodItems(Resource):

    def get(self):
        if not food_items:
            return {"massage": "food_items are not created yed"}, 200
        return {"Food_items": food_items}, 200

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("food_name",
                            type=str,
                            required=True,
                            help="The food_name field can't be empty",
                            location='json')
        parser.add_argument("description",
                            required=True,
                            type=str,

                            help="The description field can't be empty")
        parser.add_argument("price",
                            type=int,
                            required=True,
                            help="Price cant be coverted ")
        parser.add_argument("status",
                            type=str,
                            required=True,
                            help="The status field can't be empty")
        args = parser.parse_args()

        """auto generating food_id"""

        if len(food_items) == 0:
            food_id = len(food_items)+1
        else:
            food_id = len(food_items)+1

        """ validate data sent """

        if not args['food_name']:
            return make_response(jsonify({"message":
                                          "Add food_name"}),
                                 401)
        if not args['description']:
            return make_response(jsonify({"message":
                                          "Add descriptrion"}),
                                 401)

        if args['price'] == "":
            return make_response(jsonify({"message":
                                          "Add price"}),
                                 401)

        if args['status'] == "":
            return make_response(jsonify({"message":
                                          "Add status"}),
                                 401)

        if len(str(args['description'])) < 8:
            return {'message': 'descrition should be more than 8 characters'}, 400

        food = Food(food_id, args["food_name"],
                    args["description"], args["price"], args["status"])

        for fd in food_items:
            if args['food_name'].strip(" ") == fd['food_name'].strip(" "):
                return make_response(jsonify({"massage": "food_item has alredy been created"}), 400)
        food.create_foodItems()
        return make_response(jsonify({"massage": "food_item has been created succesfully"}), 201)
