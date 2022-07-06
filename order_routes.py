from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

from database import Session, engine
from models import Order, User
from schemas import OrderModel, OrderStatusModel

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
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        pizza_size = order.pizza_size,
        quantity = order.quantity
    )

    new_order.user = user

    session.add(new_order)
    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response) 

@order_router.get('/all')
def list_all_orders(Authorize: AuthJWT = Depends()):
    """
        ## Listing all orders
        This route lists all orders that were made. 
        Can only be accessed by superusers.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = session.query(Order).all()

        return jsonable_encoder(orders)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )

@order_router.get('/get_order/{id}')
def get_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    """
        ## Get an order by ID
        This route gets anyone's order by ID.
        Can only be accessed by superusers.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()

        return jsonable_encoder(order)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )

@order_router.get('/my_orders')
def get_user_orders(Authorize: AuthJWT = Depends()):
    """
        ## Gets all current user's orders
        This route gets all the currently logged in user's orders.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    return jsonable_encoder(user.orders)

@order_router.get('/my_orders/{id}')
def get_user_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    """
        ## Gets current user's order by id
        This route gets a currently logged in user's order by id.
        This route can only return orders that were made by the connected user.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    orders = user.orders

    for i in orders:
        if i.id == id:
            return i

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="You dont have an order with the given id"    
    )

@order_router.put('/update/{id}')
def update_order_by_id(id: int, order: OrderModel, Authorize: AuthJWT = Depends()):
    """
        ## Updates current user's order by id
        This route updates current user's order by id.
        This route requires:
        - quantity: integer
        - pizza_size: string 
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    try:
        order_to_update = session.query(Order).filter(Order.id == id).first()

        current_user = Authorize.get_jwt_subject()

        user = session.query(User).filter(User.username == current_user).first()

        if order_to_update.user_id == user.id:

            order_to_update.quantity = order.quantity
            order_to_update.pizza_size = order.pizza_size

            session.commit()

            response = {
                "id": order_to_update.id,
                "quantity": order_to_update.quantity,
                "pizza_size": order_to_update.pizza_size,
                "order_status": order_to_update.order_status
            }

            return jsonable_encoder(response)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Id"
        )
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This isn't your order"
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
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()
    
    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == id).first()

        order_to_update.order_status = order.order_status

        session.commit()

        response = {
            "id": order_to_update.id,
            "quantity": order_to_update.quantity,
            "pizza_size": order_to_update.pizza_size,
            "order_status": order_to_update.order_status
        }

        return jsonable_encoder(response)

@order_router.delete('/delete/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_an_order(id: int, Authorize: AuthJWT = Depends()):
    """
        ## Deletes an order
        This route deletes an order by id.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    order_to_delete = session.query(Order).filter(Order.id == id).first()

    session.delete(order_to_delete)

    session.commit()

    return order_to_delete