from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import check_password_hash, generate_password_hash

from database import Session, engine
from models import User
from schemas import LoginModel, SignUpModel

auth_router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

session=Session(bind=engine)


@auth_router.post('/signup', 
    status_code=status.HTTP_201_CREATED
)
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
    db_email = session.query(User).filter(User.email==user.email).first()

    if db_email:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    db_username = session.query(User).filter(User.username==user.username).first()

    if db_username:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )

    new_user = User(
        username = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )

    session.add(new_user)

    session.commit()

    return new_user

@auth_router.post('/login', status_code=status.HTTP_200_OK)
def login(user: LoginModel, Authorize: AuthJWT=Depends()):
    """
        ## Logs in a user
        This route logs in a user.
        This route requires:
        - username: string
        - password: string
    """
    db_user = session.query(User).filter(User.username==user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response = {
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response)
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Invalid Username or Password"
    )

@auth_router.get('/refresh')
def refresh_tokens(Authorize: AuthJWT = Depends()):
    """
        ## Refreshes an access token 
        This route refreshes an access token.
        This route requires:
        - refresh token
    """
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide a valid refresh token"
        )

    current_user = Authorize.get_jwt_subject()

    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access": access_token})
