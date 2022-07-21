# Pizza Delivery FastAPI

:pizza: :pizza: :pizza:

A Pizza Delivery API project built to learn FastAPI and SQLAlchemy. Uses JWT Authentication.

Scroll down to see the **Instructions** on how to launch this project properly. 

## Available Routes

| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *GET* | ```/docs/``` | _View API Documentation_|_All Users_|
| *POST* | ```/auth/signup/``` | _Sign up new User_| _All Users_|
| *POST* | ```/auth/login/``` | _Login User_|_All Users_|
| *POST* | ```/auth/refresh/``` | _Refresh JWT Access Token_|_All Users_|
| *POST* | ```/order/new_order``` | _Create an Order_|_All Users_|
| *GET* | ```/order/my_orders/``` | _Get User's Orders_|_All Users_|
| *GET* | ```/order/my_orders/{order_id}/``` | _Get User's specific Order_|_All Users_|
| *PUT* | ```/order/update/{order_id}/``` | _Update an Order_|_All Users_|
| *DELETE* | ```/order/delete/{order_id}/``` | _Delete an Order_ |_All Users_|
| *GET* | ```/order/all/``` | _List all Orders made_|_Superusers_|
| *GET* | ```/order/get_order/{order_id}/``` | _Retrieve an Order_|_Superusers_|
| *PUT* | ```/order/status/{order_id}/``` | _Update Order Status_|_Superusers_|

## Instructions

1. Clone this project
2. Start a new Virtualenv, activate it, type in console `pip install -r requirements.txt`
3. Set up a new PostgreSQL database and set its URL in `database.py`
```
engine=create_engine('postgresql://<username>:<password>@localhost/<db_name>')
```
4. Create your database by running `py init_db.py`
5. Run the API by typing in console `uvicorn main:app`

## Technologies

Backend: FastAPI v0.78, SQLAlchemy v1.4. 

Database: PostgreSQL.

## To Do/To Add

- [ ] Optimize code; 
