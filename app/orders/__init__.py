from flask import Blueprint
from .views import OrdersList, SingleOrder
from flask_restful import Api


orders = Blueprint("orders", __name__, url_prefix='/api/v1')

orders_api = Api(orders)
orders_api.add_resource(OrdersList, '/orders')
orders_api.add_resource(SingleOrder, '/orders/<int:order_id>')
