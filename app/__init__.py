from instance.config import app_config
from flask import Flask, render_template, redirect, request,jsonify


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

    @app.errorhandler(405)
    def url_not_found(error):
        return jsonify({'message':'requested url is invalid'}), 405

    @app.errorhandler(404)
    def content_not_found(error):
        return jsonify({'message':'requested url is not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message':'internal server error'}), 500



    @app.route('/')
    def index():
        return "Fast-food-Fast"
    return app
