from instance.config import app_config
from flask import Flask, render_template, redirect, request


def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    """
    registering Blueprints

    """
    from app.orders import orders as orders_blueprints
    app.register_blueprint(orders_blueprints)

    from app.food_items import food_items as food_items_blueprints
    app.register_blueprint(food_items_blueprints)

    @app.route('/')
    def index():
        return "Fast-food-Fast"
    return app
