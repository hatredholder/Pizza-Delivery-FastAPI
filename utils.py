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

def get_current_user(Authorize: AuthJWT, session: Session):
    """
        Returns JWT authorized user model
    """
    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    return user

def find_user_order(id: int, orders: Order):
    for i in orders:
        if i.id == id:
            return i
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You dont have an order with the given id"    
    )

def response_order(id: int, quantity: int, pizza_size: str, order_status: str):
    response = {
        "id": id,
        "quantity": quantity,
        "pizza_size": pizza_size,
        "order_status": order_status
    }
    return response

def check_if_pizza_size_valid(pizza_size: str):
    if pizza_size not in ['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong pizza size, available pizza sizes are: SMALL, MEDIUM, LARGE, EXTRA_LARGE"
        )