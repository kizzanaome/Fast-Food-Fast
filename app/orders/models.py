from flask import Flask

""" 
    Global variable list  holds  orders , initially its empty
    
"""
orders_db = []


class Order:
    """ Class for modeling orders """

    def __init__(self, order_id,food_id,food_name, quantity,location, status):
        """
            This method acts as a constructor
            for our class, its used to initialise class attributes
        """
        self.order_id = order_id
        self.food_id = food_id
        self.food_name = food_name.strip(" ")
        self.quantity = quantity
        self.location = location.strip(" ")
        self.status = status.strip(" ")

    def place_an_order(self):
        """ 
            This method receives an object of the 
            class, creates and returns a dictionary from the object
        """
        order = {

            "order_id": self.order_id,
            "food_id" : self.food_id,
            "food_name": self.food_name,
            "quantity": self.quantity,
            "location" : self.location,
            "status": self.status
        }

        orders_db.append(order)
        return order
