from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from models import Order, User

### auth_routes

def check_if_email_already_used(user_email: str, session: Session):
    """
        Checks if given email is already used on another account, returns an exception if it is
    """
    db_email = session.query(User).filter(User.email==user_email).first()

    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

def check_if_username_already_used(user_username: str, session: Session):
    """
        Checks if given username is already used on another account, returns an exception if it is
    """
    db_username = session.query(User).filter(User.username==user_username).first()

    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )

def create_new_user(user_username: str, user_email: str, user_password: str, user_is_staff: bool, user_is_active: bool):
    """
        Creates a new user
    """
    new_user = User(
        username = user_username,
        email = user_email,
        password = generate_password_hash(user_password),
        is_staff=user_is_staff,
        is_active=user_is_active
    )        
    return new_user

def find_user(user_username: str, session: Session):
    """
        Finds a user by given username
    """
    db_user = session.query(User).filter(User.username==user_username).first()

    return db_user

def check_if_user_exists_and_check_password(user_username, user_password, db_user: User):
    """
        Checks if user exists and checks if password is right
    """
    if not db_user or not check_password_hash(db_user.password, user_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid Username or Password"
    )

def response_token(access_token: str, refresh_token: str):
    """
        Creates an order object to return it in the route 
    """
    response = {
        "access": access_token,
        "refresh": refresh_token
    }
    return response

### order_routes

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

def check_if_order_status_valid(order_status: str):
    """
        Checks if given order_status is valid, returns exception if it isn't
    """
    if not order_status in ['PENDING', 'IN-TRANSIT', 'DELIVERED']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong order status, available statuses are: PENDING, IN-TRANSIT, DELIVERED"
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
    """
        Checks if user owns the order or if the user is a superuser, returns exception if both are false
    """
    if order_id != user_id and not is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This isn't your order"
        )

def create_new_order(pizza_size: str, quantity: int, user: User):
    """
        Creates and returns a new order
    """
    new_order = Order(
        pizza_size = pizza_size,
        quantity = quantity
    )
    new_order.user = user
    return new_order
    