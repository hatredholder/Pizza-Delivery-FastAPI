from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from models import Order, User


def jwt_required(Authorize: AuthJWT):
    """
        JWT Authentication from the fastapi_jwt_auth module
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

def find_current_user(Authorize: AuthJWT, session: Session):
    """
        Returns JWT authorized user model
    """
    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    return user

def find_user_order_by_id(id: int, session: Session):
    """
        Returns user order found by id
    """
    order = session.query(Order).filter(Order.id == id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order with the given ID doesn't exist"
        )
    return order

def response_order(id: int, quantity: int, pizza_size: str, order_status: str):
    """
        Creates an order object to return it in the route with jsonable_encoder
    """
    response = {
        "id": id,
        "quantity": quantity,
        "pizza_size": pizza_size,
        "order_status": order_status
    }
    return response

def check_if_pizza_size_valid(pizza_size: str):
    """
        Checks if given pizza_size is valid, returns exception if it isn't
    """
    if pizza_size not in ['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong pizza size, available pizza sizes are: SMALL, MEDIUM, LARGE, EXTRA_LARGE"
        )

def check_if_user_is_staff(is_staff: bool):
    """
        Checks if user is staff, returns exception if he isn't
    """
    if not is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )

def check_order_ownership_or_staff(order_id: int, user_id: int, is_staff: bool):
    if order_id != user_id and not is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This isn't your order"
        )