from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

from database import Session, engine
from models import Order
from schemas import OrderModel, OrderStatusModel
from utils import (check_if_pizza_size_valid,
                   check_if_user_is_staff, find_current_user,
                   jwt_required, response_order, check_order_ownership_or_staff, find_user_order_by_id)

order_router = APIRouter(
    prefix="/order",
    tags=['Orders']
)

session=Session(bind=engine)


@order_router.post('/new_order', status_code=status.HTTP_201_CREATED)
def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    """
        ## Placing a Order
        This route makes a new order.
        This route requires:
        - quantity: integer
        - pizza_size: string 
    """
    jwt_required(Authorize)

    user = find_current_user(Authorize, session)

    check_if_pizza_size_valid(order.pizza_size)

    new_order = Order(
        pizza_size = order.pizza_size,
        quantity = order.quantity
    )
    new_order.user = user

    session.add(new_order)
    session.commit()

    return jsonable_encoder(
        response_order(
        new_order.id, new_order.quantity, new_order.pizza_size, new_order.order_status
        )
    ) 
    
@order_router.get('/all')
def list_all_orders(Authorize: AuthJWT = Depends()):
    """
        ## Listing all orders
        This route lists all orders that were made. 
        Can only be accessed by superusers.
    """
    jwt_required(Authorize)

    user = find_current_user(Authorize, session)

    check_if_user_is_staff(user.is_staff)

    orders = session.query(Order).all()

    if not orders:
        return {"message":"No orders were made yet"}

    return jsonable_encoder(orders)

@order_router.get('/get_order/{id}')
def get_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    """
        ## Get an order by ID
        This route gets anyone's order by ID.
        Can only be accessed by superusers.
    """
    jwt_required(Authorize)

    user = find_current_user(Authorize, session)

    check_if_user_is_staff(user.is_staff)

    order = find_user_order_by_id(id, session)

    return jsonable_encoder(order)

@order_router.get('/my_orders')
def get_user_orders(Authorize: AuthJWT = Depends()):
    """
        ## Gets all current user's orders
        This route gets all the currently logged in user's orders.
    """
    jwt_required(Authorize)

    user = find_current_user(Authorize, session)

    if not user.orders:
        return {"message":"You haven't made any orders yet"}

    return jsonable_encoder(user.orders)

@order_router.get('/my_orders/{id}')
def get_user_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    """
        ## Gets current user's order by id
        This route gets a currently logged in user's order by id.
        This route can only return orders that were made by the connected user.
    """
    jwt_required(Authorize)

    user = find_current_user(Authorize, session)

    return find_user_order_by_id(id, session)


@order_router.put('/update/{id}')
def update_order_by_id(id: int, order: OrderModel, Authorize: AuthJWT = Depends()):
    """
        ## Updates current user's order by id
        This route updates current user's order by id.
        This route requires:
        - quantity: integer
        - pizza_size: string 
    """
    jwt_required(Authorize)

    order_to_update = find_user_order_by_id(id, session)

    user = find_current_user(Authorize, session)

    check_order_ownership_or_staff(order_to_update.id, user.id, user.is_staff)

    check_if_pizza_size_valid(order.pizza_size)

    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size

    session.commit()

    return jsonable_encoder(
        response_order(
        order_to_update.id, order_to_update.quantity, order_to_update.pizza_size, order_to_update.order_status
        )
    ) 

@order_router.patch('/status/{id}')
def update_order_status(id: int, order: OrderStatusModel, Authorize: AuthJWT = Depends()):
    """
        ## Updates an order's status
        This route updates an order's status by id.
        Can only be accessed by superusers.
        This route requires:
        - order_status: string
    """ 
    jwt_required(Authorize)

    user = find_current_user(Authorize, session)
    
    check_if_user_is_staff(user.is_staff)

    if order.order_status in ['PENDING', 'IN-TRANSIT', 'DELIVERED']:

        order_to_update = find_user_order_by_id(id, session)

        order_to_update.order_status = order.order_status

        session.commit()

        return jsonable_encoder(
            response_order(
            order_to_update.id, order_to_update.quantity, order_to_update.pizza_size, order_to_update.order_status)
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Wrong order status, available statuses are: PENDING, IN-TRANSIT, DELIVERED"
    )

@order_router.delete('/delete/{id}', status_code = status.HTTP_200_OK)
def delete_an_order(id: int, Authorize: AuthJWT = Depends()):
    """
        ## Deletes an order
        This route deletes an order by id if user who requested owns the order
        or the user is superuser.
    """
    jwt_required(Authorize)

    user = find_current_user(Authorize, session)

    order_to_delete = find_user_order_by_id(id, session)

    check_order_ownership_or_staff(order_to_delete.id, user.id, user.is_staff)

    session.delete(order_to_delete)
    session.commit()

    return {"message":"Order successfully deleted"}