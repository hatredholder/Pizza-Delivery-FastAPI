from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import check_password_hash

from database import Session, engine
from models import User
from schemas import LoginModel, SignUpModel
from utils import (check_if_email_already_used,
                   check_if_user_exists_and_check_password,
                   check_if_username_already_used, create_new_user, find_user,
                   response_token)

auth_router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

session=Session(bind=engine)


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
def signup(user: SignUpModel):
    """
        ## Creates a user
        This route signups a new user.
        This route requires:
        - username: string
        - email: string
        - password: string
        - is_staff: bool
        - is_active: bool
    """
    
    check_if_email_already_used(user.email, session)

    check_if_username_already_used(user.username, session)

    new_user = create_new_user(user.username, user.email, user.password, user.is_staff, user.is_active)

    session.add(new_user)
    session.commit()

    return {'message':'Success! You\'ve just signed up!'}

@auth_router.post('/login', status_code=status.HTTP_200_OK)
def login(user: LoginModel, Authorize: AuthJWT=Depends()):
    """
        ## Logs in a user
        This route logs in a user.
        This route requires:
        - username: string
        - password: string
    """
    db_user = find_user(user.username, session)

    check_if_user_exists_and_check_password(user.username, user.password, db_user)

    access_token = Authorize.create_access_token(subject=db_user.username)
    refresh_token = Authorize.create_refresh_token(subject=db_user.username)

    response = response_token(access_token, refresh_token)

    return jsonable_encoder(response)
