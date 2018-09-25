food_menu = {
    "food_id": 1,
    "food_name": "pizza",
    "price": 20000

}

post_an_order = {
    "food_name": "pizza",
    "quantity": 3,
    "location": "mutundwe",
    "status": "pending"
}

food_menu_2 = {
    "food_id": 2,
    "food_name": "Hotdog",
    "price": 20000

}
post_an_order_with_a_wrong_foodmenu_id = {
    "order_id":1,
    "food_name": "pizza",
    "quantity": 3,
    "location": "mutundwe",
    "status": "pending"
}

post_with_empty_location={
    "food_name": "pizza",
    "quantity": 3,
    "location": "",
    "status": "pending"
}

posting_wrong_datatype_for_quantity_field={
    "food_id": 3,
    "quantity": "three",
    "location": "mubende",
    "status": "pending"
}

posting_order_with_short_characters={
    "food_id": 1,
    "quantity": 3,
    "location": "kla",
    "status": "pending"
} 


posting_order_with_spaces_before_characters={
    "food_id": 1,
    "quantity": 3,
    "location": "   kampala",
    "status": "pending"
} 


posting_order_with_symbols={
    "food_id": 1,
    "quantity": 3,
    "location": "...../[]",
    "status": "pending"
} 

updated_status={
    "status":"Approved"
}

food_item={
    "food_name":"superghetti",
    "price":10000
}
