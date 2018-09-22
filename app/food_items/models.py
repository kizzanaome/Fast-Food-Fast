from flask import Flask
import string

"""
    Global variable food_items  holds  foods , initially its empty
"""

food_items = []

class Food:
    def __init__(self, food_id, food_name, price):
        """
            This method acts as a constructor
            for our class, its used to initialise class attributes
        """
        self.food_id = food_id
        self.food_name = food_name
        self.price = price

    def create_foodItems(self):
        """
            This method receives an object of the
            class, creates and returns a dictionary from the object
        """
        item = {
            "food_id" :self.food_id,
            "food_name" : self.food_name,
            "price" : self.price
        }

        food_items.append(item)
        return item

