# Pizza Delivery FastAPI

:pizza: :pizza: :pizza:

A Pizza Delivery API project built to learn FastAPI and SQLAlchemy. Uses JWT Authentication.

Scroll down to see the **Instructions** on how to launch this project properly. 

## Available Routes

| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *GET* | ```/docs/``` | _View API documentation_|_All users_|
| *POST* | ```/auth/signup/``` | _Signup new user_| _All users_|
| *POST* | ```/auth/login/``` | _Login user_|_All users_|
| *POST* | ```/auth/refresh/``` | _Refresh JWT access token_|_All users_|
| *POST* | ```/order/new_order``` | _Create an order_|_All users_|
| *GET* | ```/order/my_orders/``` | _Get user's orders_|_All users_|
| *GET* | ```/order/my_orders/{order_id}/``` | _Get user's specific order_|_All users_|
| *PUT* | ```/order/update/{order_id}/``` | _Update an order_|_All users_|
| *DELETE* | ```/order/delete/{order_id}/``` | _Delete an order_ |_All users_|
| *GET* | ```/order/all/``` | _List all orders made_|_Superuser_|
| *GET* | ```/order/get_order/{order_id}/``` | _Retrieve an order_|_Superuser_|
| *PUT* | ```/order/status/{order_id}/``` | _Update order status_|_Superuser_|

## Instructions

1. Clone this project
2. Start a new Virtualenv, activate it, type in console `pip install -r requirements.txt`
3. Set up a new PostgreSQL database and set its URL in your `database.py`
```
engine=create_engine('postgresql://postgres:<username>:<password>@localhost/<db_name>')
```
4. Create your database by running `python init_db.py`
5. Run the API by typing in console `uvicorn main:app`

## Technologies

Backend: FastAPI v0.78, SQLAlchemy v1.4. 

Database: PostgreSQL.

## To Do/To Add

- [ ] Optimize code; 
