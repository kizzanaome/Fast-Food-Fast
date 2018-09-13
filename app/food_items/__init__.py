from .views import FoodItems
from flask_restful import Api
from flask import Blueprint

food_items = Blueprint('food_items',__name__, url_prefix='/api/v1')
food_items_api = Api(food_items)

food_items_api.add_resource(FoodItems, '/food_items')